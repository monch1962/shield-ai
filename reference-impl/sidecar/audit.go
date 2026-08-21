package main

import (
	"bytes"
	"encoding/json"
	"log"
	"net/http"
	"time"
)

// AuditEvent is the sanitised, structured record written for every decision
// (MIR-01 agent activity logging, MIR-03 prompt audit log redaction, MIR-06
// forensic readiness). The sidecar emits one JSON line per decision to stdout
// (the append-only forensic store) and, when configured, forwards the same
// event to the SIEM pipeline (OTLP/HTTP bridge point in the telemetry
// architecture).
type AuditEvent struct {
	Timestamp     string   `json:"timestamp"`
	CorrelationID string   `json:"correlation_id"`
	AgentID       string   `json:"agent_id"`
	SessionID     string   `json:"session_id"`
	Tool          string   `json:"tool"`
	ActionKind    string   `json:"action_kind"`
	Verdict       string   `json:"verdict"` // allow | deny
	Denies        []string `json:"denies,omitempty"`
	DecisionMS    int64    `json:"decision_ms"`
}

type AuditSink struct {
	SIEMURL string
}

// Emit logs the event as JSONL (the forensic store) and fire-and-forgets a
// copy to the configured SIEM endpoint. Redacted by construction: the event
// carries identifiers and verdicts, never prompt/response bodies.
func (a *AuditSink) Emit(ev AuditEvent) {
	line, err := json.Marshal(ev)
	if err != nil {
		return
	}
	log.Printf("AUDIT %s", line)
	if a.SIEMURL == "" {
		return
	}
	go func() {
		client := &http.Client{Timeout: 3 * time.Second}
		req, err := http.NewRequest(http.MethodPost, a.SIEMURL, bytes.NewReader(line))
		if err != nil {
			return
		}
		req.Header.Set("Content-Type", "application/json")
		if resp, err := client.Do(req); err == nil {
			resp.Body.Close()
		}
	}()
}
