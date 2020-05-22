FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
        iputils-ping net-tools iproute2 bash nmap isc-dhcp-client \
	traceroute dnsutils lynx tcpdump ettercap-text-only \
        openssl wget unzip bsdmainutils ssh \
	netcat dns2tcp httptunnel ptunnel udptunnel \
	vim 

COPY start_app.sh .
CMD ./start_app.sh

