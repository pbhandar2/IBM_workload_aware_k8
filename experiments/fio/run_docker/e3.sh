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


# user input 
workload_name="${1:-}" # the name of the workload to identify the folder where the I/O occurs 
container_memory="${2:-}" # the memory allocated to the FIO container 
fs_memory="${3:-}" # the amount of memory allocated to the FS
mempressure_start_gb="${4:-}" # the mempressure will start with this value and end 


if [ $fs_memory -eq "0" ];
then
    FS_TYPE="page_cache"
    io_replay_log_path="/mnt/replay_logs/${workload_name}.log"
else
    # reset the page cache and the FUSE cache before starting 
    io_replay_log_path="/mnt/replay_logs/kcache_${workload_name}.log"
    fs_mountpath="/mnt/data/files/kcache_${workload_name}"
    fs_storagepath="/mnt/data/files/${workload_name}"
    ./reset_kcache.sh "${fs_mountpath}" "${fs_storagepath}" "${FS_CACHEPATH}" "${fs_memory}" "${FS_TYPE}"
fi


output_directory="/mnt/output/${workload_name}/${FS_TYPE}_mempressure"
mkdir -p "/mnt/data/output/${workload_name}/${FS_TYPE}_mempressure"


echo "Running workload: ${workload_name}, Memory: ${container_memory}"
json_output_path="${output_directory}/${container_memory}_${fs_memory}_${mempressure_start_gb}.json"
lat_output_path="${output_directory}/${container_memory}_${fs_memory}_${mempressure_start_gb}"
echo "JSON: ${json_output_path}, LAT: ${lat_output_path}"

sync; echo 3 > /proc/sys/vm/drop_caches 

docker run \
    --name="${CONTAINER_NAME}" \
    -m="${container_memory}m" \
    -v /mnt/data:/mnt \
    xridge/fio \
    --name=test \
    --read_iolog=$io_replay_log_path \
    --read_iolog_chunked=1 \
    --output-format=json --output=$json_output_path \
    --write_lat_log=$lat_output_path 


# apply mempressure after a specified period 
for sleep_time in 8000 4000 2000 1000
do
    sleep ${sleep_time}
    echo "Generating MemPressure! ${mempressure_start_gb} GB"
    memtester "${mempressure_start_gb}" &
    memtester_pid=$!
    sleep 60
    kill -9 "${memtester_pid}"
    mempressure_start_gb=$(($mempressure_start_gb-1))
done 


status_code="$(docker container wait ${CONTAINER_NAME})"
echo "Status code of last run command: ${status_code}"
docker container rm ${CONTAINER_NAME}

