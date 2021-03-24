FROM ubuntu
RUN mkdir /home/data
RUN mkdir /mount
COPY ./script.sh /home/data
COPY ./workloads/seq_read_1g.job /home/data
RUN chmod +x /home/data/script.sh
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git && \ 
    apt-get install -y fio
ENTRYPOINT ["/home/data/script.sh"]


