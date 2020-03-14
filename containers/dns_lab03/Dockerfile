FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
	iputils-ping net-tools iproute2 bash bind9

COPY named.conf /etc/bind/named.conf
COPY db.10 /etc/bind/db.10

COPY start_app.sh .
CMD ./start_app.sh
