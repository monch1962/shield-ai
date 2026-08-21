package main

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"strings"
)

// Tool is a registered tool in the sidecar's gateway registry. Registration is
// explicit (TP-01); tool metadata flows into the policy input so the Rego set
// evaluates the same claims the gateway enforces (TP-02/03/04/08).
type Tool struct {
	ToolID     string   `json:"tool_id"`
	Endpoint   string   `json:"endpoint"`
	HighRisk   bool     `json:"high_risk"`
	RiskClass  string   `json:"high_risk_class"`
	Sensitive  bool     `json:"sensitive"`
	HighImpact bool     `json:"high_impact"`
	Schema     []string `json:"schema_fields"` // allowed payload fields (TP-03/04)
}

// actionClaims returns the policy-input claims the gateway asserts about this
// tool. Infrastructure control-plane APIs are never registered (EE-02, TP-08);
// anything else in the registry is explicit by construction.
func (t Tool) actionClaims() map[string]any {
	c := map[string]any{
		"tool":               t.ToolID,
		"registration":       "explicit",
		"registered_as_tool": true,
	}
	if t.HighRisk || t.HighImpact {
		c["high_impact"] = true
	}
	if t.RiskClass != "" {
		c["high_risk_class"] = t.RiskClass
	}
	if t.Sensitive {
		c["sensitive"] = true
	}
	return c
}

func loadTools(dir string) (map[string]Tool, error) {
	tools := map[string]Tool{}
	entries, err := os.ReadDir(dir)
	if err != nil {
		return nil, fmt.Errorf("read tools dir: %w", err)
	}
	for _, e := range entries {
		if e.IsDir() || !strings.HasSuffix(e.Name(), ".json") {
			continue
		}
		var t Tool
		data, err := os.ReadFile(filepath.Join(dir, e.Name()))
		if err != nil {
			return nil, err
		}
		if err := json.Unmarshal(data, &t); err != nil {
			return nil, fmt.Errorf("%s: %w", e.Name(), err)
		}
		if t.ToolID == "" {
			return nil, fmt.Errorf("%s: tool_id required", e.Name())
		}
		if _, dup := tools[t.ToolID]; dup {
			return nil, fmt.Errorf("duplicate tool registration %q", t.ToolID)
		}
		tools[t.ToolID] = t
	}
	return tools, nil
}
