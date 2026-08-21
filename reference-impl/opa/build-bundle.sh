#!/usr/bin/env bash
# Stage the 59 policy files (no tests/) and build the OPA bundle.
set -euo pipefail
cd "$(dirname "$0")/.." || exit 1  # reference-impl/

STAGE=$(mktemp -d /tmp/refimpl-stage.XXXXXX)
trap 'rm -rf "$STAGE"' EXIT
cp ../policies/*.rego "$STAGE"/

export PATH="$HOME/.local/bin:$PATH"
opa build -b "$STAGE" -o opa/bundle.tar.gz
echo "bundle written: opa/bundle.tar.gz"
