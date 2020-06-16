FROM ubuntu:bionic

LABEL version="1.0"
LABEL maintainer="Vasyl Vaskivskyi <vaskivskyi.v@gmail.com>"
LABEL description="HUBMAP imaging mass spectrometry pipeline."

RUN apt-get -qq update \
    && apt-get -qq install --no-install-recommends --yes \
    wget \
    bzip2 \
    ca-certificates \
    curl \
    unzip \
    python3 \
    python3-pip \
    openjdk-8-jre \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/
RUN python3 -m pip install --no-cache-dir setuptools
RUN python3 -m pip install --no-cache-dir -r /tmp/requirements.txt \
    && rm -rf /root/.cache/pip

# copy python scripts and download metadata extractor
COPY bin /opt/ims_pipeline/bin
RUN wget --quiet https://github.com/VasylVaskivskyi/extract_meta/releases/latest/download/extract_meta.jar -P /opt/ims_pipeline/bin/extract_meta
