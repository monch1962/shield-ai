#!/usr/bin/env bash
# SHIELD-AI reference-impl end-to-end test.
# Runs the full pipeline without containers: OPA server (bundle = ../policies),
# the sidecar, then asserts the verdict matrix across every action kind the
# policy set can gate. Each deny case asserts the deny marker of every control
# it is expected to exercise, so coverage is verifiable case by case.
set -euo pipefail

cd "$(dirname "$0")/.." || exit 1  # reference-impl/
export PATH="$HOME/.local/bin:/usr/local/go/bin:$PATH"

OPA_BIN="$(command -v opa || echo "$HOME/.local/bin/opa")"

echo "== build sidecar + mocktool =="
(cd sidecar && go build -o bin/sidecar . && go build -o bin/mocktool ./cmd/mocktool)

echo "== stage bundle (policy files only, no tests/) =="
STAGE=$(mktemp -d /tmp/refimpl-bundle.XXXXXX)
cp ../policies/*.rego "$STAGE"/

echo "== start OPA (bundle: staged 59 policies) =="
"$OPA_BIN" run --server --bundle "$STAGE" --addr 127.0.0.1:8181 \
  >/tmp/refimpl-opa.log 2>&1 &
OPA_PID=$!

echo "== start mocktool (tool endpoints + SIEM sink) =="
(cd sidecar && ./bin/mocktool >/tmp/refimpl-mock.log 2>&1) &
MOCK_PID=$!

echo "== start sidecar =="
(cd sidecar && ./bin/sidecar \
  -opa http://127.0.0.1:8181 \
  -addr 127.0.0.1:8080 \
  -agents ../agents -tools ../tools -deployment ../deployment.json \
  -siem http://127.0.0.1:8091/siem \
  >/tmp/refimpl-sidecar.log 2>&1) &
SIDE_PID=$!

trap 'kill $OPA_PID $SIDE_PID $MOCK_PID 2>/dev/null || true' EXIT

for _ in $(seq 1 40); do
  curl -sf http://127.0.0.1:8181/v1/data >/dev/null 2>&1 && break
  sleep 0.5
done
for _ in $(seq 1 40); do
  curl -sf http://127.0.0.1:8080/v1/health >/dev/null 2>&1 && break
  sleep 0.5
done

fail=0
total=0
deny_cases=0
# check <name> <expected_http> <expected_markers_pipe_separated> <input_file>
check() {
  local name="$1" want_code="$2" markers="$3" input="$4"
  local code
  total=$((total + 1))
  code=$(curl -s -o /tmp/refimpl-resp.json -w '%{http_code}' \
    -X POST http://127.0.0.1:8080/v1/decide -d @"$input")
  if [ "$code" != "$want_code" ]; then
    echo "FAIL $name: expected HTTP $want_code, got $code"
    cat /tmp/refimpl-resp.json; echo
    fail=1
    return
  fi
  if [ "$want_code" = "403" ]; then
    deny_cases=$((deny_cases + 1))
  fi
  if [ -n "$markers" ]; then
    IFS='|' read -ra want_list <<<"$markers"
    local missing=""
    for m in "${want_list[@]}"; do
      if ! grep -qF "$m" /tmp/refimpl-resp.json; then
        missing="$missing [$m]"
      fi
    done
    if [ -n "$missing" ]; then
      echo "FAIL $name: missing marker(s):$missing"
      cat /tmp/refimpl-resp.json; echo
      fail=1
      return
    fi
  fi
  echo "PASS $name (HTTP $code)${markers:+ markers: $markers}"
}

# Allow cases: the positive controls (full 59-policy evaluation must pass).
check "allow_benign"              200 "" inputs/allow_benign.json
check "allow_approved_transfer"   200 "" inputs/allow_approved_transfer.json

# Deny cases: one or more controls must fire with their deny message.
check "deny_unregistered_tool"    403 "TP-01 deny|TP-09 deny|TP-02 deny" inputs/deny_unregistered_tool.json
check "deny_unsandboxed_highrisk" 403 "EE-01 deny"                        inputs/deny_unsandboxed_highrisk.json
check "deny_injection"            403 "MS-04 deny|MS-09 deny"             inputs/deny_injection.json
check "deny_infra_api"            403 "EE-02 deny"                        inputs/deny_infra_api.json
check "deny_code_execution"       403 "EE-06 deny"                        inputs/deny_code_execution.json
check "deny_resource_exhaustion"  403 "EE-03 deny"                        inputs/deny_resource_exhaustion.json
check "deny_eval_harness"         403 "EE-04 deny|EE-08 deny|MS-07 deny"  inputs/deny_eval_harness.json
check "deny_model_deploy"         403 "MS-01 deny|MS-03 deny|MS-06 deny"  inputs/deny_model_deploy.json
check "deny_training_run"         403 "MS-02 deny|DS-05 deny"             inputs/deny_training_run.json
check "deny_ingestion"            403 "DS-01 deny|DS-02 deny"             inputs/deny_ingestion.json
check "deny_retrieval"            403 "DS-04 deny"                        inputs/deny_retrieval.json
check "deny_output_delivery"      403 "DS-06 deny|MS-05 deny"             inputs/deny_output_delivery.json
check "deny_publication"          403 "DS-07 deny"                        inputs/deny_publication.json
check "deny_mcp_connect"          403 "MS-08 deny"                        inputs/deny_mcp_connect.json
check "deny_binding"              403 "TP-10 deny"                        inputs/deny_binding.json
check "deny_document_render"      403 "TP-11 deny"                        inputs/deny_document_render.json
check "deny_log_alert"            403 "MS-11 deny"                        inputs/deny_log_alert.json
check "deny_deployment"           403 "TP-05 deny|TP-06 deny|TP-07 deny"  inputs/deny_deployment.json
check "deny_session_end"          403 "DS-03 deny|MIR-02 deny"            inputs/deny_session_end.json
check "deny_incident_unhandled"   403 "MIR-04 deny"                       inputs/deny_incident_unhandled.json
check "deny_memory_write"         403 "MS-10 deny|DS-03 deny"             inputs/deny_memory_write.json
check "deny_broken_identity"      403 "IAM-01 deny|IAM-02 deny|IAM-04 deny|IAM-05 deny|IAM-06 deny|IAM-07 deny|IAM-08 deny" inputs/deny_broken_identity.json
check "deny_highrisk_no_approval" 403 "IAM-03 deny|GRM-03 deny"           inputs/deny_highrisk_no_approval.json
check "deny_untrusted_vendor"     403 "GRM-04 deny"                       inputs/deny_untrusted_vendor.json
check "deny_bad_schema_args"      403 "TP-03 deny"                        inputs/deny_bad_schema_args.json
check "deny_file_write"           403 "EE-05 deny|EE-07 deny"             inputs/deny_file_write.json

# The deny cases must be audit-logged (MIR-01) and every decision exported to
# the SIEM sink (MIR-06 reconstruction). Counts must match the matrix exactly.
sleep 1
deny_audits=$(grep -c '"verdict":"deny"' /tmp/refimpl-sidecar.log || true)
siem_events=$(grep -c 'SIEM' /tmp/refimpl-mock.log || true)
echo "cases: $total, deny cases: $deny_cases; audit events (deny): $deny_audits, SIEM events: $siem_events"
if [ "$deny_audits" -lt "$deny_cases" ] || [ "$siem_events" -lt "$total" ]; then
  echo "FAIL: telemetry pipeline under-reported"
  fail=1
fi

if [ "$fail" -ne 0 ]; then
  echo "E2E FAILED"
  exit 1
fi
echo "E2E PASSED: all verdicts and the telemetry pipeline verified"
