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
MIN_FS_MEMORY_MB=500
MAX_FS_MEMORY_MB=2500
MEMORY_STEP=250

reset_fs() {
    fs_mountpath="${1:-}"
    fs_storage="${2:-}"
    fs_cachepath="${3:-}"
    fs_configpath="${4:-}"
    cache_size="${5:-}"

    if mountpoint -q "$fs_mountpath"; then
        echo "${fs_mountpath} is a mountpoint. Unmounting ..."
        umount "${fs_mountpath}"
    else
        echo "${fs_mountpath} is not a mountpoint"
    fi

    if mountpoint -q "${fs_cachepath}"; then
        echo "${fs_cachepath} is a mountpoint. Unmounting ..."
        umount "${fs_cachepath}"
    else
        echo "${fs_cachepath} is not a mountpoint"
    fi

    rm -rf /cache # empry the cache directory if it has leftovers 
    rm -rf "${fs_mountpath}/*" # empty the mountpath to avoid mount not empty errors 
    rm -rf "${fs_storage}/*" # empty leftover files from previous runs 

    mkdir -p /cache 
    mount -t tmpfs -o size="${cache_size}m" kcache "${fs_cachepath}"
    sleep 5 

    if [ "$cache_size" -gt 0 ]; then
        python3 "${__root}/fs/kubecachefs/KubeCacheFS.py" \
            -m "${fs_mountpath}" \
            -s "${fs_storage}" \
            -c "${fs_cachepath}" \
            -k "${fs_configpath}" &

        echo "KubeCacheFS is reset and a fresh FS is mounted!"
        sleep 15 # give the FS time to mount 
    fi

}


# user input 
workload_name="${1:-}" # the name of the workload to identify the folder where the I/O occurs 
container_memory_mb="${2:-}" # the memory allocated to the FIO container 


output_directory="/mnt/output/${workload_name}/${FS_TYPE}"
mkdir -p "/mnt/data/output/${workload_name}/${FS_TYPE}"
io_replay_log_path="/mnt/replay_logs/kcache_${workload_name}.log"


for (( fs_memory_allocation_mb=${MAX_FS_MEMORY_MB}; fs_memory_allocation_mb>=${MIN_FS_MEMORY_MB}; fs_memory_allocation_mb-=${MEMORY_STEP} ))
do
    for (( i=1; i<=$NUM_ITER; i++ ))
    do 

        echo "${i}, Running workload: ${workload_name}, FS Memory: ${fs_memory_allocation_mb}"
        json_output_path="${output_directory}/kcache_${container_memory_mb}_${fs_memory_allocation_mb}_${i}.json"
        lat_output_path="${output_directory}/kcache_${container_memory_mb}_${fs_memory_allocation_mb}_${i}"
        echo "JSON: ${json_output_path}, LAT: ${lat_output_path}"


        python3 ${__root}/fs/kubecachefs/generate_config.py ${fs_memory_allocation_mb} ${FS_TYPE}
        FS_CONFIGPATH="${__root}/fs/kubecachefs/config/lru_${FS_TYPE}_${fs_memory_allocation_mb}.json"
        reset_fs "/mnt/data/files/kcache_${workload_name}" "/mnt/data/files/${workload_name}" \
            "${FS_CACHEPATH}" "${FS_CONFIGPATH}" "${fs_memory_allocation_mb}"


        # reset the page cache before starting docker 
        sync; echo 3 > /proc/sys/vm/drop_caches 
        docker run \
            --name="${CONTAINER_NAME}" \
            -m="${container_memory_mb}m" \
            -v /mnt/data:/mnt \
            xridge/fio \
            --name=test \
            --read_iolog=${io_replay_log_path} \
            --read_iolog_chunked=1 \
            --output-format=json --output=${json_output_path} \
            --write_lat_log=${lat_output_path} 


        status_code="$(docker container wait ${CONTAINER_NAME})"
        echo "Status code of last run command: ${status_code}"
        docker container rm ${CONTAINER_NAME}
        
    done 
done 
