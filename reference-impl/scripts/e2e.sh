#!/usr/bin/env bash
# SHIELD-AI reference-impl end-to-end test.
# Runs the full pipeline without containers: OPA server (bundle = ../policies),
# the sidecar, then asserts verdicts on the six sample inputs.
set -euo pipefail

cd "$(dirname "$0")/.." || exit 1  # reference-impl/
export PATH="$HOME/.local/bin:$PATH"

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
# check <name> <expected_http> <expected_substring> <input_file>
check() {
  local name="$1" want_code="$2" want_text="$3" input="$4"
  local code
  code=$(curl -s -o /tmp/refimpl-resp.json -w '%{http_code}' \
    -X POST http://127.0.0.1:8080/v1/decide -d @"$input")
  if [ "$code" != "$want_code" ]; then
    echo "FAIL $name: expected HTTP $want_code, got $code"
    cat /tmp/refimpl-resp.json; echo
    fail=1
    return
  fi
  if [ -n "$want_text" ] && ! grep -q "$want_text" /tmp/refimpl-resp.json; then
    echo "FAIL $name: missing '$want_text' in response"
    cat /tmp/refimpl-resp.json; echo
    fail=1
    return
  fi
  echo "PASS $name (HTTP $code)"
}

check "allow_benign"              200 ""                         inputs/allow_benign.json
check "allow_approved_transfer"   200 ""                         inputs/allow_approved_transfer.json
check "deny_unregistered_tool"    403 "TP-01 deny"                inputs/deny_unregistered_tool.json
check "deny_unsandboxed_highrisk" 403 "EE-01 deny"                inputs/deny_unsandboxed_highrisk.json
check "deny_injection"            403 "MS-04 deny"                inputs/deny_injection.json
check "deny_infra_api"            403 "EE-02 deny"                inputs/deny_infra_api.json

# The deny cases must be audit-logged (MIR-01) and exported to the SIEM sink.
sleep 1
deny_audits=$(grep -c '"verdict":"deny"' /tmp/refimpl-sidecar.log || true)
siem_events=$(grep -c 'SIEM' /tmp/refimpl-mock.log || true)
echo "audit events (deny): $deny_audits, SIEM events: $siem_events"
if [ "$deny_audits" -lt 4 ] || [ "$siem_events" -lt 6 ]; then
  echo "FAIL: telemetry pipeline under-reported"
  fail=1
fi

if [ "$fail" -ne 0 ]; then
  echo "E2E FAILED"
  exit 1
fi
echo "E2E PASSED: all verdicts and the telemetry pipeline verified"
