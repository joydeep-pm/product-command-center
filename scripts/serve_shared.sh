#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
node webapp/server.js
