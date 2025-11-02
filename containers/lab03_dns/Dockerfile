FROM cdci_base

COPY named.conf /etc/bind/named.conf
COPY db.10 /etc/bind/db.10

COPY start_app.sh .
CMD ./start_app.sh
