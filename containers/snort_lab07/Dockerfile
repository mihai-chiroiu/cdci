FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
        iputils-ping net-tools iproute2 bash openssl wget unzip bsdmainutils ssh vim curl \
        python-setuptools \
        python-pip \
        python-dev \
        wget \
        build-essential \
        bison automake \
        flex \
        libpcap-dev \
        libpcre3-dev \
        libdumbnet-dev \
        zlib1g-dev \
        iptables-dev \
        libnetfilter-queue1 \
        tcpdump \
        unzip \
        vim \ 
	libluajit-5.1-dev pkg-config openssl libssl-dev

# Define working directory.
WORKDIR /opt

ENV DAQ_VERSION 2.0.7
RUN wget https://www.snort.org/downloads/snort/daq-${DAQ_VERSION}.tar.gz \
    && tar xvfz daq-${DAQ_VERSION}.tar.gz \
    && cd daq-${DAQ_VERSION} \
    && ./configure; make; make install

RUN ldconfig

ENV SNORT_VERSION 2.9.16
RUN wget https://www.snort.org/downloads/snort/snort-${SNORT_VERSION}.tar.gz \
    && tar xvfz snort-${SNORT_VERSION}.tar.gz \
    && cd snort-${SNORT_VERSION} \
    && ./configure; make; make install

RUN ldconfig

RUN mkdir -p /etc/snort/rules \
    && curl -sSL https://www.snort.org/downloads/community/community-rules.tar.gz | \
       tar xz --strip 1 -C /etc/snort/rules/ community-rules/community.rules \
    && touch /etc/snort/rules/local.rules \
             /etc/snort/rules/black_list.rules \
             /etc/snort/rules/white_list.rules \
    && mkdir -p /etc/snort/so_rules \
                /etc/snort/preproc_rules \
                /usr/local/lib/snort_dynamicrules \
    && ln -s /usr/lib64/libdnet.so.1 /usr/local/lib/libdnet.1 

ADD snortconf /opt 

RUN mkdir -p /var/log/snort && \
    mkdir -p /usr/local/lib/snort_dynamicrules && \
    mkdir -p /etc/snort && \

    # snortconfig rules
    cp -r /opt/rules /etc/snort/rules && \
    # Due to empty folder so mkdir
    mkdir -p /etc/snort/preproc_rules && \
    mkdir -p /etc/snort/so_rules && \
    cp -r /opt/etc/* /etc/snort/. && \

    # touch /etc/snort/rules/local.rules && \
    touch /etc/snort/rules/white_list.rules /etc/snort/rules/black_list.rules

COPY start_app.sh .
CMD ./start_app.sh
