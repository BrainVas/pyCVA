
FROM continuumio/miniconda3


ENV ENV_NAME cave_env


RUN apt-get update && apt-get install -y \
    libpng-dev \
    libtiff-dev \
    libjpeg-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY environmentCAVE.yml .

RUN conda env create -n $ENV_NAME -f environmentCAVE.yml && conda clean -afy

ENV PATH /opt/conda/envs/$ENV_NAME/bin:$PATH

WORKDIR /app

COPY . .

# docker run --rm `
#    -v "${PWD}/input_dicom:/app/input_dicom" `
#    -v "${PWD}/output_masks:/app/output_masks" `
#    -v "${PWD}/checkpoints:/app/checkpoints" `
#    cave_docker `
#    input_dicom/SN3_Vap_SOP1.2.826.0.1.3680043.9.6827.2401407280984092171337075126937802959.dcm `
#    output_masks/output_mask.png `
#    checkpoints/minip_av_sigmoid_image1024_valiant-resonance-1199.pt `
#    --input-type minip `
#    --label-type av `
#    --img_size 1024 
