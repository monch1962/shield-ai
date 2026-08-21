package main

import (
	"crypto/rand"
	"encoding/hex"
	"encoding/json"
	"log"
	"net/http"
	"time"
)

// Sidecar entry point. The sidecar is the Zone 2 enforcement point: it carries
// the tool gateway, the policy input enricher, and the telemetry exporter, and
// evaluates every agent action against the Zone 3 OPA decision point before
// the action is permitted. Every verdict is an audit event.

func main() {
	cfg := parseConfig()

	enricher, err := NewEnricher(cfg.DeploymentFile, cfg.AgentsDir, cfg.ToolsDir)
	if err != nil {
		log.Fatalf("enricher init: %v", err)
	}
	sink := &AuditSink{SIEMURL: cfg.SIEMURL}

	log.Printf("SHIELD-AI reference sidecar listening on %s (OPA: %s, SIEM: %q)",
		cfg.ListenAddr, cfg.OPAURL, cfg.SIEMURL)
	log.Fatal(http.ListenAndServe(cfg.ListenAddr, newDecisionHandler(cfg, enricher, sink)))
}

// newDecisionHandler wires the sidecar's HTTP surface. Exposed for tests.
func newDecisionHandler(cfg Config, enricher *Enricher, sink *AuditSink) http.Handler {
	mux := http.NewServeMux()

	mux.HandleFunc("GET /v1/health", func(w http.ResponseWriter, r *http.Request) {
		_, err := Evaluate(r.Context(), cfg.OPAURL, map[string]any{
			"agent":  map[string]any{"id": "__health__"},
			"action": map[string]any{"tool": "__health__"},
		})
		status := "ok"
		if err != nil {
			status = "opa_unreachable"
		}
		writeJSON(w, http.StatusOK, map[string]any{"status": status, "opa": err == nil})
	})

	// POST /v1/decide -- evaluate one agent action against the full policy set.
	mux.HandleFunc("POST /v1/decide", func(w http.ResponseWriter, r *http.Request) {
		r.Body = http.MaxBytesReader(w, r.Body, 1<<20)
		var req map[string]any
		if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
			writeJSON(w, http.StatusBadRequest, map[string]any{"error": "invalid request body"})
			return
		}
		input, err := enricher.Enrich(req)
		if err != nil {
			writeJSON(w, http.StatusBadRequest, map[string]any{"error": err.Error()})
			return
		}
		if cfg.Debug {
			dbg, _ := json.Marshal(input)
			log.Printf("DEBUG input: %s", dbg)
		}
		start := time.Now()
		verdict, err := Evaluate(r.Context(), cfg.OPAURL, input)
		ms := time.Since(start).Milliseconds()
		if err != nil {
			// Fail closed: an unreachable policy engine blocks the action.
			verdict = &Verdict{Allowed: false, Denies: []string{"policy engine unreachable (fail closed): " + err.Error()}}
		}
		if cfg.Debug {
			dbg, _ := json.Marshal(verdict)
			log.Printf("DEBUG verdict: %s", dbg)
		}
		cid := newCorrelationID()
		ev := AuditEvent{
			Timestamp:     time.Now().UTC().Format(time.RFC3339),
			CorrelationID: cid,
			AgentID:       agentID(req),
			SessionID:     sessionID(input),
			Tool:          actionTool(req),
			ActionKind:    actionKind(req),
			Verdict:       map[bool]string{true: "allow", false: "deny"}[verdict.Allowed],
			Denies:        verdict.Denies,
			DecisionMS:    ms,
		}
		sink.Emit(ev)

		if !verdict.Allowed {
			writeJSON(w, http.StatusForbidden, map[string]any{
				"allowed": false, "correlation_id": cid, "denies": verdict.Denies,
			})
			return
		}
		writeJSON(w, http.StatusOK, map[string]any{
			"allowed": true, "correlation_id": cid, "denies": []string{},
		})
	})

	return mux
}

func writeJSON(w http.ResponseWriter, code int, v any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(code)
	_ = json.NewEncoder(w).Encode(v)
}

func newCorrelationID() string {
	b := make([]byte, 8)
	if _, err := rand.Read(b); err != nil {
		return "cid-unknown"
	}
	return "cid-" + hex.EncodeToString(b)
}

func agentID(req map[string]any) string {
	if a, ok := req["agent"].(map[string]any); ok {
		if id, ok := a["id"].(string); ok {
			return id
		}
	}
	return ""
}

func sessionID(input map[string]any) string {
	if a, ok := input["action"].(map[string]any); ok {
		if p, ok := a["provenance"].(map[string]any); ok {
			if s, ok := p["session"].(string); ok {
				return s
			}
		}
	}
	return ""
}

func actionTool(req map[string]any) string {
	if a, ok := req["action"].(map[string]any); ok {
		if t, ok := a["tool"].(string); ok {
			return t
		}
	}
	return ""
}

func actionKind(req map[string]any) string {
	if a, ok := req["action"].(map[string]any); ok {
		if k, ok := a["kind"].(string); ok {
			return k
		}
	}
	return ""
}
