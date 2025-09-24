import subprocess
import os
from src.build import build_project

class OMPRunner:
    """
    Runner for the OpenMP benchmark binary.
    """

    def __init__(self, project_dir="src/omp", exe_name="omp_bench"):
        self.project_dir = os.path.abspath(project_dir)
        self.exe_path = os.path.join(self.project_dir, "build", exe_name)

    def build(self):
        print("[OMP] Building...")
        build_project(self.project_dir)
        print("[OMP] Build complete.")

    def run(self, N: int) -> int:
        result = subprocess.run(
            [self.exe_path, str(N)],
            capture_output=True,
            text=True,
            check=True
        )
        return int(result.stdout.strip())
