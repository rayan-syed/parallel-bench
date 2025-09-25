import subprocess
import os
from src.build import build_project

llvm_icd  = "/usr/share/vulkan/icd.d/lvp_icd.x86_64.json"
swiftshader_icd = "externals/SwiftShader/build/Linux/vk_swiftshader_icd.json"

class WGPURunner:
    """
    Runner for the WebGPU benchmark binary.
    """

    def __init__(self, backend=None):
        self.backend = backend
        self.project_dir = os.path.abspath("src/wgpu")
        self.build_dir = "build"
        self.exe_path = os.path.join(self.project_dir, self.build_dir,"wgpu")
        if backend == "llvmpipe":
            self.icd = llvm_icd
        elif backend == "swiftshader":
            self.icd = swiftshader_icd
        else:
            self.icd = None

    def build(self):
        """Build the WGPU C++ project."""
        print(f"[WGPU] Building...")
        build_project(self.project_dir, self.build_dir)
        print(f"[WGPU] Build complete.")

    def run(self, N: int) -> int:
        """Run WGPU binary with N and return avg time in ms."""
        env = os.environ.copy()
        if self.icd:
            env["VK_ICD_FILENAMES"] = self.icd
        result = subprocess.run(
            [self.exe_path, str(N)],
            capture_output=True,
            text=True,
            check=True,
            env=env
        )
        return int(result.stdout.strip())
