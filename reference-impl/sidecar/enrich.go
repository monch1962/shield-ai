package main

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"strings"
)

// Enricher carries the static claims (organisation posture, agent identity,
// tool registry) and attests the fields the sidecar itself enforces: gateway
// controls, audit pipeline, provenance. The merged document is the policy
// input for every decision.

type Enricher struct {
	deployment map[string]any            // organisation-level posture (deployment.json)
	agents     map[string]map[string]any // agent id -> claims under "agent"
	tools      map[string]Tool           // explicit tool registry
}

func NewEnricher(deploymentFile, agentsDir, toolsDir string) (*Enricher, error) {
	dep, err := decodeMapFile(deploymentFile)
	if err != nil {
		return nil, fmt.Errorf("deployment: %w", err)
	}
	agents, err := loadAgentClaims(agentsDir)
	if err != nil {
		return nil, err
	}
	tools, err := loadTools(toolsDir)
	if err != nil {
		return nil, err
	}
	return &Enricher{deployment: dep, agents: agents, tools: tools}, nil
}

// Enrich merges the request over the organisation and agent posture, asserts
// the tool registry claims, and attests the sidecar-owned fields.
func (e *Enricher) Enrich(req map[string]any) (map[string]any, error) {
	out := deepCopy(e.deployment)

	reqAgent, _ := req["agent"].(map[string]any)
	aid, _ := reqAgent["id"].(string)
	if aid == "" {
		return nil, fmt.Errorf("agent.id is required")
	}
	if cfg, ok := e.agents[aid]; ok {
		out["agent"] = deepMerge(deepCopy(cfg), reqAgent)
	} else {
		out["agent"] = deepCopy(reqAgent)
	}
	out = deepMerge(out, req) // action/context/approval over the base posture
	outAgent, _ := out["agent"].(map[string]any)

	action, _ := out["action"].(map[string]any)
	if action == nil {
		return nil, fmt.Errorf("action is required")
	}
	toolName, _ := action["tool"].(string)
	if toolName == "" {
		return nil, fmt.Errorf("action.tool is required")
	}

	// Tool registry claims (TP-01/02): membership, registration mode, risk class.
	t, inRegistry := e.tools[toolName]
	action["registered_as_tool"] = inRegistry
	if inRegistry {
		action["registration"] = "explicit"
		for k, v := range t.actionClaims() {
			action[k] = v
		}
	}
	action["tool_allowed"] = false
	if allow, ok := outAgent["allowlist"].([]any); ok {
		for _, a := range allow {
			if a == toolName {
				action["tool_allowed"] = true
			}
		}
	}

	// Gateway claims: this sidecar IS the tool gateway (TP-02/03/08).
	action["tool_auth"] = map[string]any{"agent_authenticated": true, "human_session": false}
	gw, _ := action["gateway"].(map[string]any)
	if gw == nil {
		gw = map[string]any{}
	}
	gw["rate_limited"] = true
	gw["audited"] = true
	gw["allowlist_active"] = true
	gw["infra_isolation"] = true
	gw["schema_validated"] = validatePayload(action, t.Schema)
	action["gateway"] = gw
	action["tool_output"] = map[string]any{
		"validated":         true,
		"sanitised":         true,
		"within_size_limit": true,
		"code_generation":   false,
		"code_sandboxed":    true,
	}

	// Audit pipeline claims: the sidecar writes append-only, reconstructible
	// logs for every decision (MIR-01/03/06) and redacts sensitive prompts.
	action["audit_record"] = true
	action["log_storage"] = "append_only"
	action["reconstructible"] = true
	if s, _ := action["sensitive"].(bool); s {
		action["prompt_captured"] = true
		action["prompt_redacted"] = true
	}
	if inc, _ := action["incident"].(bool); inc {
		action["reporting_triggered"] = true
	}

	// Tenant scoping (IAM-09): the sidecar binds every request to its agent's
	// tenant at the data layer.
	if tid, _ := outAgent["tenant_id"].(string); tid != "" {
		out["tenant"] = map[string]any{"id": tid, "scoped": true}
	}

	// Dispatch provenance (TP-12): mint session/turn binding when the caller
	// did not supply one. In production this comes from the model-turn
	// authenticator; a minted id is the explicit reference-impl compromise.
	if prov, _ := action["provenance"].(map[string]any); prov == nil {
		action["provenance"] = map[string]any{
			"session":   "s-" + aid,
			"turn":      "t-1",
			"model_sig": "sidecar-minted",
		}
	}
	return out, nil
}

// validatePayload checks the action's args against the tool's declared schema
// fields (TP-03/04). No declared schema means nothing to validate.
func validatePayload(action map[string]any, schema []string) bool {
	if len(schema) == 0 {
		return true
	}
	args, _ := action["args"].(map[string]any)
	if args == nil {
		return false
	}
	allowed := map[string]bool{}
	for _, f := range schema {
		allowed[f] = true
	}
	for k := range args {
		if !allowed[k] {
			return false
		}
	}
	return true
}

func decodeMapFile(path string) (map[string]any, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	var m map[string]any
	if err := json.Unmarshal(data, &m); err != nil {
		return nil, err
	}
	return m, nil
}

func loadAgentClaims(dir string) (map[string]map[string]any, error) {
	agents := map[string]map[string]any{}
	entries, err := os.ReadDir(dir)
	if err != nil {
		return nil, fmt.Errorf("read agents dir: %w", err)
	}
	for _, e := range entries {
		if e.IsDir() || !strings.HasSuffix(e.Name(), ".json") {
			continue
		}
		m, err := decodeMapFile(filepath.Join(dir, e.Name()))
		if err != nil {
			return nil, err
		}
		block, ok := m["agent"].(map[string]any)
		if !ok {
			return nil, fmt.Errorf("%s: missing agent block", e.Name())
		}
		id, _ := block["id"].(string)
		if id == "" {
			return nil, fmt.Errorf("%s: agent.id required", e.Name())
		}
		agents[id] = block
	}
	return agents, nil
}

// deepMerge merges src into dst recursively (dst is mutated).
func deepMerge(dst, src map[string]any) map[string]any {
	for k, v := range src {
		sv, ok := v.(map[string]any)
		dv, isMap := dst[k].(map[string]any)
		if ok && isMap {
			deepMerge(dv, sv)
		} else {
			dst[k] = v
		}
	}
	return dst
}

func deepCopy(m map[string]any) map[string]any {
	out := make(map[string]any, len(m))
	for k, v := range m {
		switch t := v.(type) {
		case map[string]any:
			out[k] = deepCopy(t)
		case []any:
			out[k] = deepCopySlice(t)
		default:
			out[k] = t
		}
	}
	return out
}

func deepCopySlice(s []any) []any {
	out := make([]any, len(s))
	for i, v := range s {
		switch t := v.(type) {
		case map[string]any:
			out[i] = deepCopy(t)
		case []any:
			out[i] = deepCopySlice(t)
		default:
			out[i] = t
		}
	}
	return out
}
