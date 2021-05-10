FROM mongo
COPY mongo-entrypoint.sh /mongo-entrypoint.sh 
COPY run_workload.sh /exec_script.sh 
ENTRYPOINT ["/usr/bin/env"]
CMD ["/mongo-entrypoint.sh", "mongod"]
