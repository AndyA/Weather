#!/bin/bash

set -ex

DATADIR="/data/grafana/loki"

mkdir -p "$DATADIR"

podman run            \
  --name loki         \
  -p 3100:3100        \
  -d grafana/loki:latest

  # -v "$DATADIR:/loki" \