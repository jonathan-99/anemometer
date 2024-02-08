#!/bin/bash

set -eu -o pipefail # fail on error and report it, debug all lines

sudo -n true
test $? -eq 0 || exit 1 "you should have sudo privilege to run this script"

# change to 'test_*' for full output
python3 -m unittest discover -s 'testing/' -v -p 'test_all.py'

# install and run coverage
pip install coverage
coverage run -m unittest discover -s 'testing/' -v -p 'test_all.py'
coverage html -d coverage_report