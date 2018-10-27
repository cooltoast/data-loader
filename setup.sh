#!/usr/bin/env bash

echo "Creating database..."
createdb <DATABASE>

echo "Initializing tables..."
psql -q -d <DATABASE> -f init.sql
