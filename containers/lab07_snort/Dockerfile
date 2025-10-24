FROM cdci_base

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends  \
        wget unzip bsdmainutils ssh vim curl \
        python3-pip \
	python-dev-is-python3 \
        wget \
        build-essential \
        bison automake \
        flex \
        libpcap-dev \
	libtirpc-dev libnsl-dev \
        libpcre3-dev \
        libdumbnet-dev \
        zlib1g-dev \
	libxtables-dev \
        libnetfilter-queue1 \
        unzip \
        vim \ 
	libluajit-5.1-dev pkg-config openssl libssl-dev

# Define working directory.
WORKDIR /opt

ENV DAQ_VERSION=2.0.7
RUN wget https://www.snort.org/downloads/snort/daq-${DAQ_VERSION}.tar.gz \
    && tar xvfz daq-${DAQ_VERSION}.tar.gz \
    && cd daq-${DAQ_VERSION} \
    && ./configure; make; make install

RUN ldconfig

ENV SNORT_VERSION=2.9.19
RUN wget https://www.snort.org/downloads/archive/snort/snort-${SNORT_VERSION}.tar.gz \
    && tar xvfz snort-${SNORT_VERSION}.tar.gz \
    && cd snort-${SNORT_VERSION} \
    && CPPFLAGS="-I/usr/include/tirpc" LDFLAGS="-ltirpc" \
    ./configure --enable-sourcefire \
    && make -j"$(nproc)" \
    && make install

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
