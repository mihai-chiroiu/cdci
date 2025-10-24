FROM cdci_base
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get -y install python3-flask python3-mysqldb mysql-server

COPY app.py .
ENV HOME /root
COPY start_app.sh .
CMD ./start_app.sh 
