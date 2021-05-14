#!/usr/bin/env bash
# Bash3 Boilerplate. Copyright (c) 2014, kvz.io

set -o errexit
set -o pipefail
set -o nounset
# set -o xtrace


# Set magic variables for current file & dir
__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
__file="${__dir}/$(basename "${BASH_SOURCE[0]}")"
__base="$(basename ${__file} .sh)"
__root="$(cd "$(dirname $(dirname $(dirname "${__dir}")))" && pwd)" # <-- change this as it depends on your app


# user input
cachepath="${1:-}"
fs_memory_mb="${2:-}"

if mountpoint -q "${cachepath}"; then
    echo "${cachepath} is a mountpoint. Unmounting ..."
    umount "${cachepath}"
else
    echo "${cachepath} is not a mountpoint"
fi

rm -rf "${cachepath}"
mkdir -p "${cachepath}"

mount -t tmpfs -o size="${fs_memory_mb}m" kcache "${cachepath}"

sleep 5 # wait fot 5 seconds just to make sure the FS is mounted and ready for use 
