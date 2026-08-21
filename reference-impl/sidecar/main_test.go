package main

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"os"
	"strings"
	"testing"
)

// --- deepMerge / deepCopy ---

func TestDeepMergeNested(t *testing.T) {
	dst := map[string]any{"a": map[string]any{"b": 1, "c": 2}, "keep": true}
	src := map[string]any{"a": map[string]any{"c": 3, "d": 4}, "new": "x"}
	out := deepMerge(dst, src)
	a := out["a"].(map[string]any)
	if a["b"] != 1 || a["c"] != 3 || a["d"] != 4 {
		t.Fatalf("merge wrong: %v", a)
	}
	if out["keep"] != true || out["new"] != "x" {
		t.Fatalf("top-level merge wrong: %v", out)
	}
}

func TestDeepCopyIsolation(t *testing.T) {
	orig := map[string]any{"a": map[string]any{"b": []any{"x", "y"}}}
	cpy := deepCopy(orig)
	cpy["a"].(map[string]any)["b"].([]any)[0] = "z"
	if orig["a"].(map[string]any)["b"].([]any)[0] != "x" {
		t.Fatal("deepCopy not isolated")
	}
}

// --- registry ---

func TestLoadToolsRejectsDuplicate(t *testing.T) {
	dir := t.TempDir()
	writeTestFile(t, dir+"/a.json", `{"tool_id": "dup", "schema_fields": ["q"]}`)
	writeTestFile(t, dir+"/b.json", `{"tool_id": "dup", "schema_fields": ["q"]}`)
	if _, err := loadTools(dir); err == nil {
		t.Fatal("expected duplicate registration error")
	}
}

// --- aggregation over the OPA result tree ---

func TestAggregateDenyWins(t *testing.T) {
	tree := map[string]any{
		"tp": map[string]any{
			"tool_inventory_and_registry": map[string]any{
				"allow": false,
				"deny":  []any{"TP-01 deny: tool \"drop_database\" is not in the approved tool registry"},
			},
		},
		"ms": map[string]any{
			"adversarial_robustness": map[string]any{"allow": true, "deny": []any{}},
		},
	}
	v := aggregate(tree)
	if v.Allowed {
		t.Fatal("deny must win over allow")
	}
	if len(v.Denies) != 1 || !strings.Contains(v.Denies[0], "TP-01 deny") {
		t.Fatalf("denies wrong: %v", v.Denies)
	}
}

func TestAggregateAllAllow(t *testing.T) {
	tree := map[string]any{
		"ee": map[string]any{
			"execution_environment_boundary": map[string]any{"allow": true, "deny": []any{}},
		},
	}
	v := aggregate(tree)
	if !v.Allowed {
		t.Fatal("expected allow")
	}
}

// Real OPA response shape: when a deny fires, `allow` is absent from the
// result tree (allow if count(deny) == 0 is undefined), not false.
func TestAggregateDenyWithAbsentAllow(t *testing.T) {
	tree := map[string]any{
		"tp": map[string]any{
			"tool_inventory_and_registry": map[string]any{
				"deny": []any{"TP-01 deny: tool \"drop_database\" is not in the approved tool registry"},
			},
		},
		"ms": map[string]any{
			"adversarial_robustness": map[string]any{"allow": true, "deny": []any{}},
		},
	}
	v := aggregate(tree)
	if v.Allowed {
		t.Fatal("deny with absent allow must block (fail closed)")
	}
	if len(v.Denies) != 1 || !strings.Contains(v.Denies[0], "TP-01 deny") {
		t.Fatalf("denies wrong: %v", v.Denies)
	}
}

func TestAggregateNoPackagesFailsClosed(t *testing.T) {
	v := aggregate(map[string]any{"result": "nothing evaluated"})
	if v.Allowed {
		t.Fatal("no evaluated packages must fail closed")
	}
}

// --- enrichment ---

func newTestEnricher(t *testing.T) *Enricher {
	t.Helper()
	e, err := NewEnricher("../deployment.json", "../agents", "../tools")
	if err != nil {
		t.Fatalf("enricher: %v", err)
	}
	return e
}

func TestEnrichBenignTool(t *testing.T) {
	e := newTestEnricher(t)
	in, err := e.Enrich(map[string]any{
		"agent":  map[string]any{"id": "agent-billing"},
		"action": map[string]any{"kind": "tool_call", "tool": "search_documents", "args": map[string]any{"query": "invoices"}},
	})
	if err != nil {
		t.Fatalf("enrich: %v", err)
	}
	a := in["action"].(map[string]any)
	if a["registered_as_tool"] != true || a["registration"] != "explicit" || a["tool_allowed"] != true {
		t.Fatalf("registry claims wrong: %v", a)
	}
	gw := a["gateway"].(map[string]any)
	if gw["allowlist_active"] != true || gw["infra_isolation"] != true || gw["schema_validated"] != true {
		t.Fatalf("gateway claims wrong: %v", gw)
	}
	if a["audit_record"] != true || a["log_storage"] != "append_only" {
		t.Fatalf("audit claims wrong: %v", a)
	}
	ag := in["agent"].(map[string]any)
	if ag["sandboxed"] != true {
		t.Fatalf("agent claims wrong: %v", ag)
	}
	ten := in["tenant"].(map[string]any)
	if ten["id"] != "acme-billing" || ten["scoped"] != true {
		t.Fatalf("tenant claims wrong: %v", ten)
	}
}

func TestEnrichHighRiskTool(t *testing.T) {
	e := newTestEnricher(t)
	in, err := e.Enrich(map[string]any{
		"agent":  map[string]any{"id": "agent-billing"},
		"action": map[string]any{"kind": "tool_call", "tool": "transfer_funds", "args": map[string]any{"amount": 5000, "to_account": "acc-9"}},
	})
	if err != nil {
		t.Fatalf("enrich: %v", err)
	}
	a := in["action"].(map[string]any)
	if a["high_risk_class"] != "financial" || a["high_impact"] != true || a["sensitive"] != true {
		t.Fatalf("tool risk claims wrong: %v", a)
	}
	if a["prompt_captured"] != true || a["prompt_redacted"] != true {
		t.Fatalf("sensitive prompt audit claims wrong: %v", a)
	}
}

func TestEnrichUnregisteredTool(t *testing.T) {
	e := newTestEnricher(t)
	in, err := e.Enrich(map[string]any{
		"agent":  map[string]any{"id": "agent-billing"},
		"action": map[string]any{"kind": "tool_call", "tool": "drop_database", "args": map[string]any{}},
	})
	if err != nil {
		t.Fatalf("enrich: %v", err)
	}
	a := in["action"].(map[string]any)
	if a["registered_as_tool"] != false || a["tool_allowed"] != false {
		t.Fatalf("unregistered claims wrong: %v", a)
	}
}

func TestEnrichMissingAgentID(t *testing.T) {
	e := newTestEnricher(t)
	if _, err := e.Enrich(map[string]any{"action": map[string]any{"tool": "x"}}); err == nil {
		t.Fatal("expected error for missing agent.id")
	}
}

func TestValidatePayload(t *testing.T) {
	if validatePayload(map[string]any{"args": map[string]any{"query": "q"}}, []string{"query"}) != true {
		t.Fatal("valid payload rejected")
	}
	if validatePayload(map[string]any{"args": map[string]any{"query": "q", "rm -rf /": 1}}, []string{"query"}) != false {
		t.Fatal("undeclared field accepted")
	}
	if validatePayload(map[string]any{}, nil) != true {
		t.Fatal("no schema should trivially pass")
	}
}

// --- HTTP decision endpoint with a stub OPA ---

func TestDecideHTTPAllow(t *testing.T) {
	opa := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		_ = json.NewEncoder(w).Encode(map[string]any{
			"result": map[string]any{
				"tp":  map[string]any{"tool_inventory_and_registry": map[string]any{"allow": true, "deny": []any{}}},
				"ee":  map[string]any{"execution_environment_boundary": map[string]any{"allow": true, "deny": []any{}}},
				"ms":  map[string]any{"adversarial_robustness": map[string]any{"allow": true, "deny": []any{}}},
				"iam": map[string]any{"human_oversight_controls": map[string]any{"allow": true, "deny": []any{}}},
			},
		})
	}))
	defer opa.Close()

	e, err := NewEnricher("../deployment.json", "../agents", "../tools")
	if err != nil {
		t.Fatal(err)
	}
	cfg := Config{OPAURL: opa.URL}
	srv := newDecisionHandler(cfg, e, &AuditSink{})

	req := httptest.NewRequest(http.MethodPost, "/v1/decide", strings.NewReader(`{
		"agent": {"id": "agent-billing"},
		"action": {"kind": "tool_call", "tool": "search_documents", "args": {"query": "invoices"}}
	}`))
	rec := httptest.NewRecorder()
	srv.ServeHTTP(rec, req)
	if rec.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d: %s", rec.Code, rec.Body.String())
	}
	var out map[string]any
	_ = json.Unmarshal(rec.Body.Bytes(), &out)
	if out["allowed"] != true {
		t.Fatalf("expected allowed=true: %v", out)
	}
}

func TestDecideHTTPDeny(t *testing.T) {
	opa := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		_ = json.NewEncoder(w).Encode(map[string]any{
			"result": map[string]any{
				"tp": map[string]any{
					"tool_inventory_and_registry": map[string]any{
						"allow": false,
						"deny":  []any{"TP-01 deny: tool \"drop_database\" is not in the approved tool registry"},
					},
				},
			},
		})
	}))
	defer opa.Close()

	e, err := NewEnricher("../deployment.json", "../agents", "../tools")
	if err != nil {
		t.Fatal(err)
	}
	cfg := Config{OPAURL: opa.URL}
	srv := newDecisionHandler(cfg, e, &AuditSink{})

	req := httptest.NewRequest(http.MethodPost, "/v1/decide", strings.NewReader(`{
		"agent": {"id": "agent-billing"},
		"action": {"kind": "tool_call", "tool": "drop_database"}
	}`))
	rec := httptest.NewRecorder()
	srv.ServeHTTP(rec, req)
	if rec.Code != http.StatusForbidden {
		t.Fatalf("expected 403, got %d", rec.Code)
	}
	var out map[string]any
	_ = json.Unmarshal(rec.Body.Bytes(), &out)
	denies := out["denies"].([]any)
	if len(denies) == 0 || !strings.Contains(denies[0].(string), "TP-01 deny") {
		t.Fatalf("denies wrong: %v", out)
	}
}

func TestDecideHTTPEngineDownFailsClosed(t *testing.T) {
	opa := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {}))
	opa.Close() // engine gone

	e, err := NewEnricher("../deployment.json", "../agents", "../tools")
	if err != nil {
		t.Fatal(err)
	}
	cfg := Config{OPAURL: opa.URL}
	srv := newDecisionHandler(cfg, e, &AuditSink{})

	req := httptest.NewRequest(http.MethodPost, "/v1/decide", strings.NewReader(`{
		"agent": {"id": "agent-billing"},
		"action": {"kind": "tool_call", "tool": "search_documents"}
	}`))
	rec := httptest.NewRecorder()
	srv.ServeHTTP(rec, req)
	if rec.Code != http.StatusForbidden {
		t.Fatalf("engine down must fail closed (403), got %d", rec.Code)
	}
	if !strings.Contains(rec.Body.String(), "fail closed") {
		t.Fatalf("expected fail-closed message: %s", rec.Body.String())
	}
}

func writeTestFile(t *testing.T, path, content string) {
	t.Helper()
	if err := os.WriteFile(path, []byte(content), 0o600); err != nil {
		t.Fatal(err)
	}
}
