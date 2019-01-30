#!/usr/bin/env bash

# Usage: sync_sources.sh remote_user@remote_host remote/path/to/directory remote_password

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )"/../.. >/dev/null 2>&1 && pwd )"
REMOTE_PATH="${1}:${2}"
sshpass -p "${3}" ssh "${1}" rm -rf ${2}/app ${2}/scripts
sshpass -p "${3}" scp -r ${BASEDIR}/app ${REMOTE_PATH}/app
sshpass -p "${3}" scp -r ${BASEDIR}/scripts ${REMOTE_PATH}/scripts
sshpass -p "${3}" ssh "${1}" tree "${2}"
