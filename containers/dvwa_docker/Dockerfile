FROM ubuntu:trusty
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install -y iputils-ping net-tools iproute2 bash
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
    debconf-utils && \
    echo mysql-server-5.5 mysql-server/root_password password vulnerables | debconf-set-selections && \
    echo mysql-server-5.5 mysql-server/root_password_again password vulnerables | debconf-set-selections && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    apache2 \
    mysql-server \
    php5 \
    php5-mysql \
    php-pear \
    php5-gd
COPY php.ini /etc/php5/apache2/php.ini
RUN apt-get -y install git 
RUN git clone --recursive https://github.com/ethicalhack3r/DVWA.git
RUN mv DVWA/* /var/www/html
RUN rm -rf DVWA
RUN chown www-data:www-data -R /var/www/html && \
    rm /var/www/html/index.html
COPY config.inc.php /var/www/html/config/.
COPY init_mysql.sql .
COPY start_app.sh .
CMD ./start_app.sh 
#CMD service apache2 start && service mysql start && mysql < init_mysql.sql && /bin/bash
#RUN apt-get -y install wget unzip git dialog systemd
#RUN apt-get -y install apache2 mysql-server php php-mysqli php-gd libapache2-mod-php
