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
mountpath="${1:-}"
storagepath="${2:-}"
cachepath="${3:-}"
memory_mb="${4:-}"
fs_type="${5:-}"

if mountpoint -q "${mountpath}"; then
    echo "${mountpath} is a mountpoint. Unmounting ..."
    umount "${mountpath}"
else
    echo "${mountpath} is not a mountpoint"
fi

rm -rf "${mountpath}"
mkdir -p "${mountpath}"

rm -rf "${storagepath}"
mkdir -p "${storagepath}"

./reset_tmpfs.sh "${cachepath}" "${memory_mb}"

python3 ${__root}/fs/kubecachefs/generate_config.py ${memory_mb} ${fs_type}
fs_configpath="${__root}/fs/kubecachefs/config/lru_${FS_TYPE}_${fs_memory_allocation_mb}.json"

python3 "${__root}/fs/kubecachefs/KubeCacheFS.py" \
    -m "${mountpath}" \
    -s "${storagepath}" \
    -c "${cachepath}" \
    -k "${fs_configpath}" &

echo "KubeCacheFS is reset and a fresh FS is mounted!"
sleep 15 # give the FS time to mount 
