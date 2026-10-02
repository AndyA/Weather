#!/bin/bash

set -ex

DATADIR="/home/andy/dev.bbcgenome.com/couchdb"

mkdir -p "$DATADIR"

podman run                        \
  --name couchdb2                 \
  -p 5985:5984                    \
  -e COUCHDB_USER="chaise"        \
  -e COUCHDB_PASSWORD="sofa"      \
  -v "$DATADIR:/opt/couchdb/data" \
  -v "$PWD/vm.args:/opt/couchdb/etc/vm.args" \
  -d couchdb

