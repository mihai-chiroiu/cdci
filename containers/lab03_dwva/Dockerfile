FROM cdci_base
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      apache2 php php-mysqli php-gd php-zip php-curl php-mbstring php-xml \
      mariadb-server git ca-certificates \
 && update-ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Enable Apache mods
RUN a2enmod php8.3 && a2enmod rewrite

# Get DVWA
RUN rm -rf /var/www/html/* \
 && git clone --depth=1 https://github.com/digininja/DVWA.git /var/www/html \
 && chown -R www-data:www-data /var/www/html \
 && sed -i 's/AllowOverride None/AllowOverride All/g' /etc/apache2/apache2.conf


# Copy your config + init SQL if you have them
COPY config.inc.php /var/www/html/config/
COPY init_mysql.sql /root/init_mysql.sql
COPY start_app.sh /usr/local/bin/start_app.sh
RUN chmod +x /usr/local/bin/start_app.sh
CMD ["/usr/local/bin/start_app.sh"]

