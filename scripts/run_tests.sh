#!/usr/bin/env bash

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )"/.. >/dev/null 2>&1 && pwd )"
export PYTHONPATH=$PYTHONPATH:$BASEDIR

python3 -u $BASEDIR/tests/run_tests.py
