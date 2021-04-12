We evaluate page cache performance in this experiment.


First, we want to evaluate how the memory allocated to a container influences 
the I/O performance. We measure this using different FIO workloads. 


docker run \
    -m="500m" \
    -v /home/oem/IBM_workload_aware_k8/experiments/page_cache/pv:/home \
    xridge/fio \
    /home/workloads/w1.fio --output-format=json --output=/home/results/w1_500.json \
    --write_lat_log=/home/lat_log/w1_500


docker run \
    -m="600m" \
    -v /home/oem/IBM_workload_aware_k8/experiments/page_cache/pv:/home \
    xridge/fio \
    /home/workloads/w2.fio --output-format=json --output=/home/results/w2_600.json \
    --write_lat_log=/home/lat_log/w2_600

