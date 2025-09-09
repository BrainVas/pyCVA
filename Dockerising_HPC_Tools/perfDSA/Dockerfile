FROM continuumio/miniconda3


ENV ENV_NAME perfDSA

RUN apt-get update && apt-get install -y \
    libpng-dev \
    libtiff-dev \
    libjpeg-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY environment.yml .

RUN conda env create -n $ENV_NAME -f environment.yml && conda clean -afy

ENV PATH /opt/conda/envs/$ENV_NAME/bin:$PATH

WORKDIR /app

COPY . .