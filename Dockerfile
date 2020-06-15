FROM continuumio/miniconda3:4.8.2

LABEL version="1.0"
LABEL maintainer="Vasyl Vaskivskyi <vaskivskyi.v@gmail.com>"
LABEL description="HUBMAP imaging mass spectrometry pipeline."

# create conda environment from yaml file
COPY environment.yml /tmp/
RUN conda env create -f /tmp/environment.yml && \
    conda clean --index-cache --tarballs --yes
RUN echo "source activate hubmap" > ~/.bashrc
ENV PATH /opt/conda/envs/hubmap/bin:$PATH

# copy python scripts and download metadata extractor 
COPY bin /opt/ims_pipeline/bin
RUN wget --quiet https://github.com/VasylVaskivskyi/extract_meta/releases/latest/download/extract_meta.jar -P /opt/ims_pipeline/bin/extract_meta
