# SHIELD-AI local gates
#
# Run `make check` before any commit; run `make build` for the full artifact
# pipeline (tools/update_all.sh: schema+Rego, diagrams, PDF/EPUB, decks, gates).
# The cheap gates here are the same ones the cron cycles run; keeping them
# one command away means no edit ships without a local gate pass.

SHELL := /bin/bash
PY    ?= python3
OPA   ?= $(shell command -v opa 2>/dev/null || echo $(HOME)/.local/bin/opa)
SKILL_SCRIPTS := $(HOME)/.hermes/profiles/sec-arch/skills/research/threat-informed-architecture-review/scripts

.PHONY: help check rego-schema lint-spacing verify catalog gap-format dna latency framework-format test-gates test build

help:
	@echo "SHIELD-AI local gates"
	@echo "  make check         regenerate schema/Rego, then run all gates (lint-spacing, verify, catalog, OPA tests)"
	@echo "  make rego-schema   regenerate control schema JSON + Rego stubs (non-destructive: preserves implemented controls)"
	@echo "  make lint-spacing  pandoc list-merge scan (repo-wide)"
	@echo "  make verify        artifact verification (footers, counts, schema drift, PDF markers, deck manifests)"
	@echo "  make catalog       exploit catalog integrity gate (G-ID to entry 1:1, link resolution)"
	@echo "  make gap-format    gap analysis format check"
	@echo "  make dna           evolution DNA gate (new threat classes absorbed or re-attested)"
	@echo "  make latency       incident latency ledger (publication -> record KPIs, backdate-proof)"
	@echo "  make framework-format  framework.md control layout gate (scannable controls, persists)"
	@echo "  make feed-misfits  external feed harvester + misfit-ratchet gate (per-lineage provenance)"
	@echo "  make test-gates    replay evolution-gate antagonisms (prove protections still fire)"
	@echo "  make test          OPA policy tests (policies/tests + demo/tests)"
	@echo "  make build         full artifact pipeline (tools/update_all.sh)"

check: rego-schema lint-spacing verify catalog gap-format dna feed-misfits latency framework-format test test-gates
	@echo ""
	@echo "All gates passed."

rego-schema:
	$(PY) tools/generate_control_schema.py --rego

lint-spacing:
	$(PY) $(SKILL_SCRIPTS)/list_spacing_scan.py .

verify:
	$(PY) tools/verify_artifacts.py

catalog:
	$(PY) tools/check_exploit_catalog.py

gap-format:
	$(PY) tools/check_gap_analysis_format.py

dna:
	$(PY) tools/check_evolution_dna.py

latency:
	$(PY) tools/latency_ledger.py

framework-format:
	$(PY) tools/check_framework_format.py

feed-misfits:
	$(PY) tools/check_feed_misfits.py
	$(PY) tools/collect_feed.py >/dev/null

test-gates:
	$(PY) tools/test_evolution_gates.py

test:
	$(OPA) test policies policies/tests demo/policies demo/tests

build:
	bash tools/update_all.sh
