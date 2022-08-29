#!/bin/bash
SCRIPT_DIR="$(dirname "$0")"

python "$SCRIPT_DIR"/../manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 2 > "$SCRIPT_DIR"/mock-data.json