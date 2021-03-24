FROM ubuntu:18.04
RUN apt-get update && \
    apt-get install -y fio

RUN mkdir data && \
    fio --name=test --directory=/data --rw=randread --filesize=5000Mi --io_size=1000Mi

VOLUME /data
