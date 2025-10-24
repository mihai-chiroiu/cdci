FROM cdci_base

RUN apt-get update && apt-get install -y \
        wget unzip bsdmainutils ssh vim

COPY start_app.sh .
CMD ./start_app.sh
