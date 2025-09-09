import os
import subprocess
from pycva.common.containerised_tool_base import ContainerisedToolBase
import sys

class autotici_wrapper(ContainerisedToolBase):

    # Wrapper for running the AutoTICI tool via Docker or Singularity containers.


    def __init__(self):
        
        # Initializes the AutoTICI_Wrapper with Docker and Singularity configurations.
        
        docker_image = "jamesboogaard/autotici_docker:latest"
        sif_name = "autotici.sif"
        super().__init__(docker_image, sif_name)

    def _run_docker(self, pre_image, post_image, occ, output_dir,
                    model_dir, motion_correction=False,
                    preregistration=False, view=None):

        # Runs AutoTICI via Docker.

        # Args:
        #     pre_image (str): Path to the PreEVT DICOM file.
        #     post_image (str): Path to the PostEVT DICOM file.
        #     occ (str): Occlusion site label (e.g. M1, ICA).
        #     output_dir (str): Path to the output directory.
        #     model_dir (str, optional): Path to the directory containing model files. Defaults to None.
        #     motion_correction (bool, optional): Enable motion correction. Defaults to False.
        #     preregistration (bool, optional): Enable preregistration. Defaults to False.
        #     view (str, optional): Specific angiographic view to use. Defaults to None.

        # Raises:
        #     subprocess.CalledProcessError: If Docker command execution fails.

        os.makedirs(output_dir, exist_ok=True)
        docker_cmd = [
            "docker", "run", "--rm",
            "-v", f"{os.path.abspath(os.path.dirname(pre_image))}:/app/pre",
            "-v", f"{os.path.abspath(os.path.dirname(model_dir))}:/app/models",
            "-v", f"{os.path.abspath(os.path.dirname(post_image))}:/app/post",
            "-v", f"{os.path.abspath(output_dir)}:/app/output"
        ]
        docker_cmd += [
            self.docker_image,
            "python", "autoTICI.py",
            f"/app/pre/{os.path.basename(pre_image)}",
            f"/app/post/{os.path.basename(post_image)}",
            occ
        ]
        if motion_correction:
            docker_cmd.append("-m")
        if preregistration:
            docker_cmd.append("-l")
        if view:
            docker_cmd += ["-v", view]
        docker_cmd += ["-o", "/app/output"]

        print(f"[DOCKER] Running: {' '.join(docker_cmd)}")
        subprocess.run(docker_cmd, check=True)

    def _run_singularity(self, pre_image, post_image, occ, output_dir,
                         model_dir=None, motion_correction=False,
                         preregistration=False, view=None):
        
        # Runs AutoTICI via Singularity.

        # Args:
        #     pre_image (str): Path to the PreEVT DICOM file.
        #     post_image (str): Path to the PostEVT DICOM file.
        #     occ (str): Occlusion site label (e.g. M1, ICA).
        #     output_dir (str): Path to the output directory.
        #     model_dir (str, optional): Path to the directory containing model files. Defaults to None.
        #     motion_correction (bool, optional): Enable motion correction. Defaults to False.
        #     preregistration (bool, optional): Enable preregistration. Defaults to False.
        #     view (str, optional): Specific angiographic view to use. Defaults to None.

        # Raises:
        #     subprocess.CalledProcessError: If Singularity command execution fails.
        
        os.makedirs(output_dir, exist_ok=True)
        binds = [
            f"{os.path.abspath(os.path.dirname(pre_image))}:/app/pre",
            f"{os.path.abspath(os.path.dirname(post_image))}:/app/post",
            f"{os.path.abspath(output_dir)}:/app/output"
        ]
        if model_dir:
            binds.append(f"{os.path.abspath(model_dir)}:/app/models")

        singularity_cmd = ["singularity", "exec","--nv"] #Enable gpu capablilities
        for b in binds:
            singularity_cmd += ["--bind", b]

        singularity_cmd += [
            self.sif_path,
            "python", "autotici.py",
            f"/app/pre/{os.path.basename(pre_image)}",
            f"/app/post/{os.path.basename(post_image)}",
            occ
        ]
        if motion_correction:
            singularity_cmd.append("-m")
        if preregistration:
            singularity_cmd.append("-l")
        if view:
            singularity_cmd += ["-v", view]
        singularity_cmd += ["-o", "/app/output"]

        print(f"[SINGULARITY] Running: {' '.join(singularity_cmd)}")
        subprocess.run(singularity_cmd, check=True)

    def run(self, *args, **kwargs):
        
        # Runs AutoTICI using either Docker or Singularity, depending on availability.

        # This method delegates to `_run_docker` or `_run_singularity` based on the
        # runtime environment.

        # Args:
        #     *args: Positional arguments passed to the container execution method.
        #     **kwargs: Keyword arguments passed to the container execution method.

        # Raises:
        #     RuntimeError: If neither Docker nor Singularity is available.
        
        return super().run(*args, **kwargs)
