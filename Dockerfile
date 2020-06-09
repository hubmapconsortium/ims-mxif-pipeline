FROM continuumio/miniconda3:4.8.2

LABEL version="1.0"
LABEL maintainer="Vasyl Vaskivskyi <vaskivskyi.v@gmail.com>"
LABEL description="HUBMAP imaging mass spectrometry pipeline."

# update OS package
RUN apt-get update && \
    apt-get install -y unzip

# import conda environment from yaml file
COPY environment.yml /tmp/
RUN conda env create -f /tmp/environment.yml
RUN echo "source activate hubmap" > ~/.bashrc
ENV PATH /opt/conda/envs/hubmap/bin:$PATH


COPY bin ims_pipeline/bin


RUN wget --quiet https://github.com/VasylVaskivskyi/extract_meta/releases/download/v1.0.1/extract_meta.jar -P /opt/ims_pipeline/bin/extract_meta/

