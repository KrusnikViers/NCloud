#!/usr/bin/env bash

# Usage: sync_run.sh remote_user@remote_host remote/path/to/directory remote_password

sshpass -p "${3}" ssh "${1}" ${2}/scripts/run.sh
