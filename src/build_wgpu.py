import subprocess
import os
import sys

def build_wgpu():
    """Build the WGPU executable"""
    wgpu_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wgpu")
    
    try:
        # Run cmake configure
        subprocess.run(["cmake", "-B", "build", "-S", "."], 
                      cwd=wgpu_dir, check=True)
        
        # Run cmake build
        subprocess.run(["cmake", "--build", "build"], 
                      cwd=wgpu_dir, check=True)
        
        print("WGPU build completed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        return False

if __name__ == "__main__":
    if build_wgpu():
        sys.exit(0)
    else:
        sys.exit(1)