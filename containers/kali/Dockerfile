FROM kalilinux/kali 

RUN apt-get update && apt-get install -y \
        iputils-ping net-tools iproute2 bash nmap isc-dhcp-client \
	traceroute dnsutils lynx tcpdump ettercap-text-only \
	vim 

CMD ["/bin/bash"]

