#Normal
FROM continuumio/miniconda3

#For apple
#FROM --platform=linux/amd64 continuumio/miniconda3

ENV ENV_NAME autotici_env

ENV MODEL_DIR=/app/models

RUN apt-get update && apt-get install -y \
    libpng-dev \
    libtiff-dev \
    libjpeg-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY environmentAu.yml .

RUN conda env create -n $ENV_NAME -f environmentAu.yml && conda clean -afy

ENV PATH /opt/conda/envs/$ENV_NAME/bin:$PATH

WORKDIR /app

COPY . .

ENV PYTHONPATH=/app:$PYTHONPATH



# docker run --rm `
# >>   -v "${PWD}/input_images:/app/input_images" `
# >>   -v "${PWD}/output:/app/output" `
# >>   -v "${PWD}/models:/app/models" `
# >>   autotici3_docker `
# >>   -v ap `
# >>   input_images/SN3_Vap_SOP1.2.826.0.1.3680043.9.6827.2401407280984092171337075126937802959.dcm `
# >>   input_images/SN10_Vap_SOP1.2.826.0.1.3680043.9.6827.2619603212203373380215256193355264957.dcm `
# >>   ICA