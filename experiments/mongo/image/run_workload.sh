#!/usr/bin/env bash
# Bash3 Boilerplate. Copyright (c) 2014, kvz.io

set -o errexit
set -o pipefail
set -o nounset
# set -o xtrace


# these directories are relative to the container volume mount inside /output 
LOAD_DATA_DIR="/output/tmp_mongo"
OUTPUT_DIR="/output" 


# user input
workload_name="${1:-}"
record_count="${2:-}"
op_count="${3:-}"
workload_tag="${4:-}"


# create relevant directories if they don't exist 
mkdir -p "${LOAD_DATA_DIR}" 
mkdir -p "${OUTPUT_DIR}" 


# download YCSB workload repo
cd /home 
apt-get -y -q update 
apt install -y -q maven curl python 
curl -O --location https://github.com/brianfrankcooper/YCSB/releases/download/0.5.0/ycsb-0.5.0.tar.gz
tar xfvz ycsb-0.5.0.tar.gz
cd ycsb-0.5.0


# run the workload
./bin/ycsb load mongodb-async -s -P "workloads/workload${workload_name}" \
    -p recordcount="${record_count}" \
    -p operationcount="${op_count}" \
    -p fieldcount=64 \
    -p fieldlength=64 > "${LOAD_DATA_DIR}/Load.txt"


./bin/ycsb run mongodb-async -s -P "workloads/workload${workload_name}" \
    -p recordcount="${record_count}" \
    -p operationcount="${op_count}" \
    -p fieldcount=64 \
    -p fieldlength=64 > "${OUTPUT_DIR}/${workload_name}_${record_count}_${op_count}_${workload_tag}"