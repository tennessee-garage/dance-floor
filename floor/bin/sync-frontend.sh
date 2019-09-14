#!/bin/bash
set -e

BUILD_DIR=$1
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
OUTPUT_DIR="${SCRIPT_DIR}/../floor/server/static"

usage() {
  echo "Usage: $0 <path/to/ddfui/build>"
}

if [ ! -e ${BUILD_DIR} ]; then
  echo "Error: Build dir '${BUILD_DIR}' not found"
  usage
  exit 1
fi

rsync -av --delete-after "${BUILD_DIR}" "${OUTPUT_DIR}"
