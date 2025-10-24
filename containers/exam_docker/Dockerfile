FROM cdci_base

RUN apt-get update && apt-get install -y \
        nmap isc-dhcp-client \
	traceroute lynx ettercap-text-only \
        wget unzip bsdmainutils ssh \
	dns2tcp httptunnel ptunnel udptunnel \
	vim 

COPY start_app.sh .
CMD ./start_app.sh

