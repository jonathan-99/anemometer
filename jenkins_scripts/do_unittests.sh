#!/bin/bash

set -eu -o pipefail # fail on error and report it, debug all lines

sudo -n true
test $? -eq 0 || exit 1 "you should have sudo privilege to run this script"

container_name=$('anemometer-test')

# PEP8 report
docker exec $CONTAINER_ID sh -c 'command -v pep8 >/dev/null 2>&1 || { apt-get update && apt-get install -y python3-pep8; } && pep8 /path/to/your/directory'

# change to 'test_*' for full output
# need to change test_all to test_*
docker exec $CONTAINER_ID python3 -m unittest discover -s 'testing/' -v -p 'test_all.py'

# this is a coverage report
docker exec $CONTAINER_ID coverage html -d coverage_report

docker exec $CONTAINER_ID sh -c 'command -v pip >/dev/null 2>&1 || { echo >&2 "pip is not installed. Installing..."; apt-get update && apt-get install -y python3-pip; }; pip freeze | tee requirements.txt'
