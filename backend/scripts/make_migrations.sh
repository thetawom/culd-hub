#!/bin/bash
SCRIPT_DIR="$(dirname "$0")"

LOAD_DATA=false

while getopts 'clh' OPTION; do
  case "$OPTION" in
    c)
      "$SCRIPT_DIR"/clean_migrations.sh
      ;;
    l)
      LOAD_DATA=true
      ;;
    ?)
      echo 'script usage: $(basename \$0) [-c] [-l]' >&2
      exit 1
      ;;
  esac
done
shift "$(($OPTIND -1))"

python "$SCRIPT_DIR"/../manage.py makemigrations
python "$SCRIPT_DIR"/../manage.py migrate

if [ "$LOAD_DATA" = true ]; then
  python "$SCRIPT_DIR"/../manage.py loaddata "$SCRIPT_DIR"/mock-data.json
fi

exit 0
