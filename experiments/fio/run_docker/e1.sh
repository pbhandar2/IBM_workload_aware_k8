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


# constant 
FS_TYPE="basic"
CONTAINER_NAME="fio-test"
FS_CACHEPATH="/cache" # the directory where the tmpfs is mounted and where KubeCacheFS stores its data 
NUM_ITER=5
MIN_MEMORY_MB=500
MAX_MEMORY_MB=3500
MEMORY_STEP=250


# user input 
workload_name="${1:-}" # the name of the workload to identify the folder where the I/O occurs 


output_directory="/mnt/output/${workload_name}/page_cache"
mkdir -p "/mnt/data/output/${workload_name}/page_cache"
io_replay_log_path="/mnt/replay_logs/${workload_name}.log"


for (( memory_allocation_mb=${MAX_MEMORY_MB}; memory_allocation_mb>=${MIN_MEMORY_MB}; memory_allocation_mb-=${MEMORY_STEP} ))
do
    for (( i=1; i<=$NUM_ITER; i++ ))
    do 

        echo "${i}, Running workload: ${workload_name}, Memory: ${memory_allocation_mb}"
        json_output_path="${output_directory}/${memory_allocation_mb}_${i}.json"
        lat_output_path="${output_directory}/${memory_allocation_mb}_${i}"
        echo "JSON: ${json_output_path}, LAT: ${lat_output_path}"


        # reset the page cache before starting docker 
        sync; echo 3 > /proc/sys/vm/drop_caches 


        docker run \
            --name="${CONTAINER_NAME}" \
            -m="${memory_allocation_mb}m" \
            -v /mnt/data:/mnt \
            xridge/fio \
            --name=test \
            --read_iolog=$io_replay_log_path \
            --read_iolog_chunked=1 \
            --output-format=json --output=$json_output_path \
            --write_lat_log=$lat_output_path 


        status_code="$(docker container wait ${CONTAINER_NAME})"
        echo "Status code of last run command: ${status_code}"

        docker container rm ${CONTAINER_NAME}
        
    done 
done 
