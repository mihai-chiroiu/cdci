FROM ubuntu:18.04
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get -y install python3-flask python3-mysqldb mysql-server
RUN apt-get install -y iputils-ping net-tools iproute2 bash
COPY app.py .
ENV HOME /root
COPY start_app.sh .
CMD ./start_app.sh 
