import subprocess
import os
from src.build import build_project

class WGPURunner:
    """
    Runner for the WebGPU benchmark binary.
    """

    def __init__(self, project_dir="src/wgpu", exe_name="wgpu"):
        self.project_dir = os.path.abspath(project_dir)
        self.exe_name = exe_name
        self.exe_path = os.path.join(self.project_dir, "build", exe_name)

    def build(self):
        """Build the WGPU C++ project."""
        build_project(self.project_dir)
        print("[WGPU] Build complete.")

    def run(self, N: int) -> int:
        """Run WGPU binary with N and return avg time in ms."""
        result = subprocess.run(
            [self.exe_path, str(N)],
            capture_output=True,
            text=True,
            check=True
        )
        return int(result.stdout.strip())
