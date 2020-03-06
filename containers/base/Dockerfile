FROM ubuntu:18.04

RUN apt-get update && apt-get install -y iputils-ping net-tools iproute2 bash

ADD infinite.sh /usr/local/bin/infinite.sh
CMD /usr/local/bin/infinite.sh

