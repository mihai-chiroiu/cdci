FROM ubuntu:18.04

RUN apt-get update && apt-get install -y iputils-ping net-tools iproute2 bash \
	dnsutils openssl tcpdump

COPY start_app.sh .
CMD ./start_app.sh 

