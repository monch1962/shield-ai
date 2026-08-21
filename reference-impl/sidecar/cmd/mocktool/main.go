// Command mocktool is the reference-impl stand-in for both the registered tool
// endpoints (proxy targets behind the gateway) and the SIEM sink. It lets the
// full pipeline run with zero external dependencies.
package main

import (
	"encoding/json"
	"io"
	"log"
	"net/http"
)

func main() {
	mux := http.NewServeMux()

	// Registered tool endpoints (what an allowed tool call would reach).
	mux.HandleFunc("/tool/", func(w http.ResponseWriter, r *http.Request) {
		body, _ := io.ReadAll(io.LimitReader(r.Body, 1<<16))
		log.Printf("mocktool %s body=%s", r.URL.Path, body)
		_ = json.NewEncoder(w).Encode(map[string]any{
			"ok":   true,
			"tool": r.URL.Path,
			"echo": json.RawMessage(body),
		})
	})

	// SIEM sink: receives audit events from the sidecar (MIR-01/03/06 export).
	mux.HandleFunc("/siem", func(w http.ResponseWriter, r *http.Request) {
		body, _ := io.ReadAll(io.LimitReader(r.Body, 1<<20))
		log.Printf("SIEM %s", body)
		w.WriteHeader(http.StatusOK)
	})

	log.Printf("mocktool listening on 0.0.0.0:8091")
	log.Fatal(http.ListenAndServe("0.0.0.0:8091", mux))
}
