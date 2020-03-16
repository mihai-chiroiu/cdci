FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
        iputils-ping net-tools iproute2 bash openssl wget unzip bsdmainutils ssh vim \
	netcat dns2tcp httptunnel ptunnel udptunnel 

COPY start_app.sh .
CMD ./start_app.sh
