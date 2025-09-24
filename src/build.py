import subprocess
import os

def build_project(project_dir: str) -> str:
    """
    Configure and build a CMake project.
    Returns path to the build directory.
    """
    build_dir = os.path.join(project_dir, "build")
    os.makedirs(build_dir, exist_ok=True)

    subprocess.run(
        ["cmake", "-S", project_dir, "-B", build_dir],
        check=True
    )
    subprocess.run(
        ["cmake", "--build", build_dir],
        check=True
    )
    return build_dir
