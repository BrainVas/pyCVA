import os
from pycva.common.containerised_tool_base import ContainerisedToolBase
import subprocess
import sys

class phase_predict_wrapper(ContainerisedToolBase):
    
    # Wrapper for running phase prediction of DICOM images using the AutoTICI docker image. 
    
    def __init__(self):
        
        # Initialises the Phase_Predict_Wrapper.
        
        docker_image="jamesboogaard/autotici_docker:latest"
        sif_name="autotici.sif"
        super().__init__(docker_image, sif_name)


    def _run_docker(self, dicom_path, output_dir, model_dir=None):
        
        # Runs phase prediction using Docker.

        # Args:
        #     dicom_path (str): Path to the input DICOM file.
        #     output_dir (str): Output directory for prediction results.
        #     model_dir (str, optional): Directory containing the model.
        
        dicom_dir = os.path.dirname(dicom_path)
        dicom_file = os.path.basename(dicom_path)

        docker_cmd = [
            "docker", "run", "--rm",
            "-v", f"{os.path.abspath(dicom_dir)}:/app/input_images",
            "-v", f"{os.path.abspath(output_dir)}:/app/output",
        ]

        if model_dir:
            docker_cmd += ["-v", f"{os.path.abspath(model_dir)}:/app/models"]

        docker_cmd += [
            self.docker_image,
            "conda", "run", "--no-capture-output", "-n", "autotici_env",
            "python", "phase_classification/phase_predict.py",
            f"input_images/{dicom_file}"
        ]

        print(f"[DOCKER] Running: {' '.join(docker_cmd)}")
        subprocess.run(docker_cmd, check=True)

    def _run_singularity(self, dicom_path, output_dir, model_dir=None):
        
        # Runs phase prediction using Singularity.

        # Args:
        #     dicom_path (str): Full path to the input DICOM file.
        #     output_dir (str): Output directory for prediction results.
        #     model_dir (str, optional): Directory containing the model.
        
        binds = [
            f"{os.path.abspath(os.path.dirname(dicom_path))}:/app/input_images",
            f"{os.path.abspath(output_dir)}:/app/output",
        
        ]

        if model_dir:
            binds.append(f"{os.path.abspath(model_dir)}:/app/models")

        singularity_cmd = [
            "singularity", "exec"
        ]
        for b in binds:
            singularity_cmd += ["--bind", b]

        singularity_cmd += [
            self.sif_path,
            "conda", "run", "--no-capture-output", "-n", "autotici_env",
            "python", "phase_classification/phase_predict.py",
            f"/app/input_images/{os.path.basename(dicom_path)}"
        ]

        print(f"[SINGULARITY] Running: {' '.join(singularity_cmd)}")
        subprocess.run(singularity_cmd, check=True)


    def run(self, *args, **kwargs):
        
        # Runs the tool using Docker or Singularity, based on what is installed.

        # Args:
        #     *args: Positional arguments to pass to the backend `_run_docker` or `_run_singularity` method.
        #     **kwargs: Keyword arguments to pass to the backend `_run_docker` or `_run_singularity` method.

        # Returns:
        #     Passes the context to the super class which decides which container tool to execute the container with (Singularity or Docker). The the implementation of _run_singularity or _run_docker is executed depending on the result.

        # Raises:
        #     RuntimeError: If neither Docker nor Singularity is installed.
        
        return super().run(*args, **kwargs)