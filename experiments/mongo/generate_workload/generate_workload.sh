#!/usr/bin/env bash
# Bash3 Boilerplate. Copyright (c) 2014, kvz.io

set -o errexit
set -o pipefail
set -o nounset
# set -o xtrace


# Set magic variables 
__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
__root="$(cd "$(dirname $(dirname $(dirname "${__dir}")))" && pwd)" 


echo "Root: ${__root} Dir: ${__dir}"

# constant 
IMAGE_NAME="my-mongo"
CONTAINER_NAME="mongo-test"
MAIN_OUTPUT_DIR="/mnt/data"
FS_MOUNTPATH="/fs-mount/"
FS_STORAGE="/fs-storage/"
MONGO_FS_LOG_OUTPUT_DIR="/mnt/data/mongo_fs_log"
WORKLOAD_TAG="0"
MONGO_OUTPUT_DIR="/mnt/data/mongo_output"


# create relevant directories if they don't exist 
mkdir -p "${MAIN_OUTPUT_DIR}"
mkdir -p "${MONGO_FS_LOG_OUTPUT_DIR}"  
mkdir -p "${FS_MOUNTPATH}"
mkdir -p "${FS_STORAGE}"
mkdir -p "${MONGO_OUTPUT_DIR}"


# user input
memory_gb="${1:-}"
workload_type="${2:-}"
record_count="${3:-}"
op_count="${4:-}"


# Reset the kcache in the specified mountpath 
reset_passthrough() {
    fs_mountpath="$1"
    fs_storage="$2"
    fs_logpath="$3"
    if mountpoint -q "$fs_mountpath"; then
        echo "$fs_mountpath is a mountpoint. Resetting ..."
        umount $fs_mountpath
    else
        echo "$fs_mountpath is not a mountpoint"
    fi

    # clean up files 
    rm -rf "${fs_storage}/*"
    rm -rf "${fs_mountpath}/*"

    # mount a fresh filesystem 
    python3 "${__root}/fs/passthrough/passthrough.py" -m "${fs_mountpath}" \
        -s "${fs_storage}" -l "${fs_logpath}" &

    echo "Fresh FS mounted!"
}


# Check for leftover exited container from previous experiment, if it exists, remove it 
if [ ! "$(docker ps -q -f name="${CONTAINER_NAME}" | grep -v ${CONTAINER_NAME})" ]; then
    echo "The container is running already!"
    if [ "$(docker ps -aq -f status=exited -f name="${CONTAINER_NAME}" | grep -v ${CONTAINER_NAME})" ]; then
        echo "Cleaning up!"
        docker rm "$CONTAINER_NAME"
    fi
fi


# reset the page cache and mount a fresh FS 
sync; echo 3 > /proc/sys/vm/drop_caches 


# setup the passthrough filesystem 
memory_mb=$((${memory_gb}*1024))
fs_logpath="${MONGO_FS_LOG_OUTPUT_DIR}/${memory_mb}_${workload_type}_${record_count}_${op_count}.csv"
reset_passthrough "${FS_MOUNTPATH}" "${FS_STORAGE}" "${fs_logpath}"


# build the container image 
cd ${__root}/experiments/mongo/image && docker build --no-cache -t "${IMAGE_NAME}" .


# setup the docker container
docker run --name "${CONTAINER_NAME}" \
    -m="${memory_mb}m" \
    -v "${FS_MOUNTPATH}":/data/db \
    -v "${MONGO_OUTPUT_DIR}":/output \
    -d "${IMAGE_NAME}" &
sleep 10 


# exec the workload script
docker exec mongo-test /bin/sh -c \
    "/exec_script.sh ${workload_type} ${record_count} ${op_count} ${WORKLOAD_TAG}" &


