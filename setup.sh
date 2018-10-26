#!/usr/bin/env bash

echo "Creating database..."
createdb clover

echo "Initializing tables..."
psql -q -d clover -f init.sql
