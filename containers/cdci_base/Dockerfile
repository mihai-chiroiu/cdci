# CDCI (c) Mihai Chiroiu 
# mihai.chiroiu@upb.ro
# https://ocw.cs.pub.ro/courses/cdci

FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      iputils-ping net-tools iproute2 bash dnsutils openssl tcpdump \
      netcat-traditional vim \
      nmap isc-dhcp-client \
      traceroute lynx ettercap-text-only \
      wget unzip bsdmainutils ssh \
      dns2tcp httptunnel ptunnel udptunnel \
      dnsmasq bind9 \
 && rm -rf /var/lib/apt/lists/*

# copy all start scripts into base image
COPY start_scripts/ /opt/start_scripts/

COPY start_cdci_base.sh /usr/local/bin/start_app.sh
CMD ["/usr/local/bin/start_app.sh"]
