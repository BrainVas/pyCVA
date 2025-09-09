import abc
import os
import shutil
import subprocess


class ContainerisedToolBase(abc.ABC):
    
    # Abstract base class to run containerised tools
    # via Docker or Singularity.
    def __init__(self, docker_image: str, sif_name: str):
        self.docker_image = docker_image
        self.sif_path = os.path.expanduser(f"~/.cache/pycva/{sif_name}")
        os.makedirs(os.path.dirname(self.sif_path), exist_ok=True)

    def docker_installed(self) -> bool:
        return shutil.which("docker") is not None

    def singularity_installed(self) -> bool:
        return shutil.which("singularity") is not None or shutil.which("apptainer") is not None

    def ensure_sif_image(self):
        if not os.path.exists(self.sif_path):
            print(f"[INFO] Pulling Singularity image for {self.docker_image}...")
            subprocess.run(
                ["singularity", "pull", self.sif_path, f"docker://{self.docker_image}"],
                check=True
            )

    def run(self, *args, **kwargs):
        
        # Run the tool using Docker or Singularity,
        # dispatching to concrete implementations of the tools.
        # Main method used by the user, takes the inputs of the tool they are trying to use.
        # Raises:
        #     RuntimeError: Specifies that neither containerisation tool is present on the current system
        # eg:        
        # Runs phase prediction using Docker or Singularity:
        
        
        # if self.docker_installed():
        #     return self._run_docker(*args, **kwargs)
        # elif self.singularity_installed():
        #     self.ensure_sif_image()
        #     return self._run_singularity(*args, **kwargs)
        # else:
        #     raise RuntimeError("Neither Docker nor Singularity is installed on the current system. In order to use this tool you need either of the afformentioned containerisation softwares.")
        
        if self.singularity_installed():
            self.ensure_sif_image()
            print("Singularity is installed")
            return self._run_singularity(*args, **kwargs)
        elif self.docker_installed():
            print("Docker is installed")
            return self._run_docker(*args, **kwargs)
        else:
            raise RuntimeError("Neither Docker nor Singularity is installed on the current system. In order to use this tool you need either of the afformentioned containerisation softwares.")

    @abc.abstractmethod
    def _run_docker(self, *args, **kwargs):
        
        # Run the tool using Docker. This method is implemented by the subclass representing the containerised tool.
        
        pass

    @abc.abstractmethod
    def _run_singularity(self, *args, **kwargs):
        
        # Run the tool using Singularity. This method is implemented by the subclass representing the containerised tool.
        
        pass
