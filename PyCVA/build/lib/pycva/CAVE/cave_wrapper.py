import os
from pycva.common.containerised_tool_base import ContainerisedToolBase
import subprocess
import sys

class cave_wrapper(ContainerisedToolBase):
    
    # Wrapper for running the CAVE tool via Docker or Singularity containers.
    
    def __init__(self):
        
        # Initializes the CAVEWrapper.
        
        docker_image = "jamesboogaard/cave_docker:latest"
        sif_name="cave.sif"
        super().__init__(docker_image,sif_name)

    def _run_docker(self, input_dicom_dir, output_masks_dir, checkpoints_dir,
                input_file, output_file, model_file,
                input_type='minip', label_type='av', img_size=1024,
                rnn='ConvGRU', rnn_kernel=1, rnn_layers=2, amp=False):
        
        # Runs the CAVE tool using Docker.
 
        # Args:
        #     input_dicom_dir (str): Directory containing input DICOM files.
        #     output_masks_dir (str): Directory to store output masks.
        #     checkpoints_dir (str): Directory containing model checkpoints (Models).
        #     input_file (str): Input DICOM filename.
        #     output_file (str): Output mask filename.
        #     model_file (str): Model file name.
        #     input_type (str): Input type for the model
        #     label_type (str): Label type for training.
        #     img_size (int): Image resolution.
        #     rnn (str): RNN type (e.g., 'ConvGRU').
        #     rnn_kernel (int): Kernel size for the RNN.
        #     rnn_layers (int): Number of RNN layers.
        #     amp (bool): Whether to use automatic mixed precision.
        

        os.makedirs(output_masks_dir, exist_ok=True)
        docker_cmd = [
            "docker", "run", "--rm",
            "-v", f"{os.path.abspath(input_dicom_dir)}:/app/input_dicom",
            "-v", f"{os.path.abspath(output_masks_dir)}:/app/output_masks",
            "-v", f"{os.path.abspath(checkpoints_dir)}:/app/checkpoints",
            self.docker_image,
            "python", "predict.py",
            f"/app/input_dicom/{input_file}",
            f"/app/output_masks/{output_file}",
            f"/app/checkpoints/{model_file}",
            "--input-type", input_type,
            "--label-type", label_type,
            "--img_size", str(img_size),
            "--rnn", rnn,
            "--rnn_kernel", str(rnn_kernel),
            "--rnn_layers", str(rnn_layers),
        ]
        if amp:
            docker_cmd.append("--amp")

        print(f"[DOCKER] Running: {' '.join(docker_cmd)}")
        subprocess.run(docker_cmd, check=True)
        

    def _run_singularity(self, input_dicom_dir, output_masks_dir, checkpoints_dir,
                         input_file, output_file, model_file,
                         input_type='minip', label_type='av', img_size=1024,
                         rnn='ConvGRU', rnn_kernel=1, rnn_layers=2, amp=False):
        
        # Runs the CAVE tool using Singularity.

        # Args:
        #     input_dicom_dir (str): Directory containing input DICOM files.
        #     output_masks_dir (str): Directory to store output masks.
        #     checkpoints_dir (str): Directory containing model checkpoints.
        #     input_file (str): Input DICOM filename.
        #     output_file (str): Output mask filename.
        #     model_file (str): Model file name.
        #     input_type (str): Input type for the model.
        #     label_type (str): Label type for training.
        #     img_size (int): Image resolution.
        #     rnn (str): RNN type (e.g., 'ConvGRU').
        #     rnn_kernel (int): Kernel size for the RNN.
        #     rnn_layers (int): Number of RNN layers.
        #     amp (bool): Whether to use automatic mixed precision.
        
        os.makedirs(output_masks_dir, exist_ok=True)
        binds = [
            f"{os.path.abspath(input_dicom_dir)}:/app/input_dicom",
            f"{os.path.abspath(output_masks_dir)}:/app/output_masks",
            f"{os.path.abspath(checkpoints_dir)}:/app/checkpoints",
        ]
        singularity_cmd = ["singularity", "exec"]
        for b in binds:
            singularity_cmd += ["--bind", b]
        singularity_cmd += [
            self.sif_path,
            "python", "predict.py",
            f"/app/input_dicom/{input_file}",
            f"/app/output_masks/{output_file}",
            f"/app/checkpoints/{model_file}",
            "--input-type", input_type,
            "--label-type", label_type,
            "--img_size", str(img_size),
            "--rnn", rnn,
            "--rnn_kernel", str(rnn_kernel),
            "--rnn_layers", str(rnn_layers),
        ]
        if amp:
            singularity_cmd.append("--amp")

        print(f"[SINGULARITY] Running: {' '.join(singularity_cmd)}")
        subprocess.run(singularity_cmd, check=True)

        
    def run(self, *args, **kwargs):
        
        # Runs the tool using Docker or Singularity, based on what is installed.

        # Args:
        #     *args: Positional arguments to pass to the backend `_run_docker` or `_run_singularity` method.
        #     **kwargs: Keyword arguments to pass to the backend `_run_docker` or `_run_singularity` method.

        # Returns:
        #     None

        # Raises:
        #     RuntimeError: If neither Docker nor Singularity is installed.
        
        return super().run(*args, **kwargs)