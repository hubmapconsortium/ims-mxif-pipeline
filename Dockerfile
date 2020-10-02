FROM ubuntu:bionic

LABEL version="1.0"
LABEL maintainer="Vasyl Vaskivskyi <vaskivskyi.v@gmail.com>"
LABEL description="HUBMAP IMS - MxIF pipeline."

RUN apt-get -qq update \
    && apt-get -qq install --no-install-recommends --yes \
    wget \
    bzip2 \
    ca-certificates \
    curl \
    unzip \
    openjdk-8-jre \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh \
    && /bin/bash /tmp/miniconda.sh -b -p /opt/conda \
    && rm /tmp/miniconda.sh
ENV PATH /opt/conda/bin:$PATH

# update base environment from yaml file
COPY environment.yml /tmp/
RUN conda env update -f /tmp/environment.yml \
    && echo "source activate base" > ~/.bashrc \
    && conda clean --index-cache --tarballs --yes
ENV PATH /opt/conda/envs/hubmap/bin:$PATH

# copy python scripts and download metadata extractor
COPY bin /opt/ims_pipeline/bin
RUN wget --quiet https://github.com/VasylVaskivskyi/extract_meta/releases/latest/download/extract_meta.jar -P /opt/ims_pipeline/bin/extract_meta
