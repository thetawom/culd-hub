#!/bin/bash
SCRIPT_DIR="$(dirname "$0")"
rm "$SCRIPT_DIR"/../**/migrations/*_initial.py
rm "$SCRIPT_DIR"/../*.sqlite3