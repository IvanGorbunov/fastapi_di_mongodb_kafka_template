#!/bin/bash

set -e
set -u
set -o pipefail

exec poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
