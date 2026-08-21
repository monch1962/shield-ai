package main

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"time"
)

// Verdict is the aggregated deny-override result across every shield_ai.*
// package. Deny wins over allow: one deny anywhere blocks the action.
type Verdict struct {
	Allowed bool     `json:"allowed"`
	Denies  []string `json:"denies"`
}

// Evaluate sends the enriched input to the OPA decision point and aggregates
// the per-package allow/deny results. Fail closed: an unreachable engine, a
// non-200 response, or a response that evaluates no policy packages denies
// the action (matching the demo's "engine unreachable = blocked" rule).
func Evaluate(ctx context.Context, opaURL string, input map[string]any) (*Verdict, error) {
	body, err := json.Marshal(map[string]any{"input": input})
	if err != nil {
		return nil, err
	}
	reqCtx, cancel := context.WithTimeout(ctx, 5*time.Second)
	defer cancel()
	req, err := http.NewRequestWithContext(reqCtx, http.MethodPost, opaURL+"/v1/data/shield_ai", bytes.NewReader(body))
	if err != nil {
		return nil, err
	}
	req.Header.Set("Content-Type", "application/json")
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return nil, fmt.Errorf("policy engine unreachable: %w", err)
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("policy engine returned HTTP %s", resp.Status)
	}
	raw, err := io.ReadAll(io.LimitReader(resp.Body, 1<<20))
	if err != nil {
		return nil, err
	}
	var doc struct {
		Result json.RawMessage `json:"result"`
	}
	if err := json.Unmarshal(raw, &doc); err != nil {
		return nil, fmt.Errorf("policy engine response parse: %w", err)
	}
	var tree any
	if err := json.Unmarshal(doc.Result, &tree); err != nil {
		return nil, fmt.Errorf("policy engine result parse: %w", err)
	}
	return aggregate(tree), nil
}

// aggregate walks the evaluated data.shield_ai tree, collecting deny messages
// from every package and requiring every allow to be true. If no package
// produced an allow verdict, the decision fails closed.
func aggregate(tree any) *Verdict {
	v := &Verdict{Allowed: true, Denies: []string{}}
	allows := 0
	var walk func(any)
	walk = func(node any) {
		m, ok := node.(map[string]any)
		if !ok {
			return
		}
		if a, ok := m["allow"].(bool); ok {
			allows++
			if !a {
				v.Allowed = false
			}
		}
		if d, ok := m["deny"].([]any); ok {
			// `allow if count(deny) == 0` means a fired deny makes allow
			// UNDEFINED (absent) in the result tree, not false. Denies win.
			if len(d) > 0 {
				v.Allowed = false
			}
			for _, msg := range d {
				if s, ok := msg.(string); ok && s != "" {
					v.Denies = append(v.Denies, s)
				}
			}
		}
		for _, child := range m {
			walk(child)
		}
	}
	walk(tree)
	if allows == 0 {
		v.Allowed = false
		v.Denies = append(v.Denies, "no policy packages evaluated (fail closed)")
	}
	return v
}
