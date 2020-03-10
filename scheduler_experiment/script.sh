#!/bin/bash
echo "Installing into a Dockerfile"
cd /home/data
dd if=/dev/urandom of=randfile bs=1M count=50 oflag=direct
fio seq_read_1g.job --output-format=json -write_lat_log=test
ls
ls -lh /mount
mv ./*.log /mount
ls -lh /mount