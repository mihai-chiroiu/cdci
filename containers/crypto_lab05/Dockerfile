FROM kalilinux/kali 

RUN apt-get update && apt-get install -y \
        iputils-ping net-tools iproute2 bash openssl

COPY start_app.sh .
CMD ./start_app.sh
