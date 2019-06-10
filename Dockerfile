FROM debian:9

RUN apt-get update -y 
RUN apt-get install -y python python-pip procps net-tools

ADD ./server /tmp/server 

RUN cd /tmp/server && \
    pip install -r requirements.txt && \
    echo 'test:90a3ed9e32b2aaf4c61c410eb925426119e1a9dc53d4286ade99a809:*' > /root/.pysock.db

WORKDIR /server
