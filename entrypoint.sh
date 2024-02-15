#!/bin/env bash
set -euo pipefail

exec uvicorn \
    --host 0.0.0.0 \
    --port 5000 \
    --factory \
    your_package.app_factory:create_app
