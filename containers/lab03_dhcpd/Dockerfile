FROM cdci_base

RUN apt-get update && apt-get install -y \
        nmap dnsmasq 

COPY dnsmasq.conf /etc/dnsmasq.conf 
COPY start_app.sh .
CMD ./start_app.sh
