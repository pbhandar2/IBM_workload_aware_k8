#!/usr/bin/env bash
# Bash3 Boilerplate. Copyright (c) 2014, kvz.io

set -o errexit
set -o pipefail
set -o nounset
# set -o xtrace


# constants 
DATA_DIR="/mnt/data/files/"
OUTPUT_DIR="/mnt/data/output"
FILE_NAME="test.0.0"


# init a file of necessary size 
workload_name="${1:-}"
file_size_gb="${2:-}"
io_size_gb="${3:-}"


# variables 
data_subdir="${DATA_DIR}/${workload_name}" 
output_subdir="${OUTPUT_DIR}/${workload_name}"


# create relevant directories if they don't exist 
mkdir -p "${data_subdir}" 
mkdir -p "${output_subdir}" 


# create the file of specified size 
dd if=/dev/urandom of="${data_subdir}/${FILE_NAME}" bs=1M count=$(($file_size_gb*1024))


# clear the page cache 
sync; echo 3 > /proc/sys/vm/drop_caches 


# read the file "N" times to generate the log 
json_output_path="${output_subdir}/${workload_name}_0_0.json"
lat_path="${output_subdir}/${workload_name}_0_0"
fio --name=test --directory="${data_subdir}" --filesize="${file_size_gb}Gi" --io_size="${io_size_gb}Gi" --rw=randread --norandommap=1 \
    --log_offset=1 --write_lat_log="${lat_path}" --output-format=json --output="${json_output_path}"







