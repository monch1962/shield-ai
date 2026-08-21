package main

import "flag"

// Config holds the sidecar's runtime wiring. Every path is relative to the
// working directory (scripts/e2e.sh and docker-compose run it from
// reference-impl/).
type Config struct {
	OPAURL         string // Zone 3 policy decision point (OPA server)
	ListenAddr     string // sidecar listen address (Zone 2)
	AgentsDir      string // directory of agent claim files (agents/*.json)
	ToolsDir       string // directory of registered tool files (tools/*.json)
	DeploymentFile string // organisation-level posture claims
	SIEMURL        string // optional audit-event sink (MIR-01/03/06 export)
	Debug          bool   // log the policy input and OPA response
}

func parseConfig() Config {
	var c Config
	flag.StringVar(&c.OPAURL, "opa", "http://127.0.0.1:8181", "OPA server base URL")
	flag.StringVar(&c.ListenAddr, "addr", "127.0.0.1:8080", "sidecar listen address")
	flag.StringVar(&c.AgentsDir, "agents", "agents", "directory of agent claim files (agents/*.json)")
	flag.StringVar(&c.ToolsDir, "tools", "tools", "directory of registered tool files (tools/*.json)")
	flag.StringVar(&c.DeploymentFile, "deployment", "deployment.json", "organisation-level posture claims")
	flag.StringVar(&c.SIEMURL, "siem", "", "optional SIEM endpoint receiving audit events")
	flag.BoolVar(&c.Debug, "debug", false, "log policy input and OPA response")
	flag.Parse()
	return c
}
