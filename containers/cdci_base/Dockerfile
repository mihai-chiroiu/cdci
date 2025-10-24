FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      iputils-ping net-tools iproute2 bash dnsutils openssl tcpdump \
      netcat-traditional vim \
 && rm -rf /var/lib/apt/lists/*

COPY start_app.sh /usr/local/bin/
CMD ["/usr/local/bin/start_app.sh"]
