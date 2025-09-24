import subprocess
import os
from build_wgpu import build_wgpu

class WGPUBenchmark:
    def __init__(self, executable_path="wgpu/build/wgpu"):
        self.executable_path = executable_path
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        
    def ensure_built(self):
        """Ensure WGPU executable is built"""
        exe_path = os.path.join(self.base_dir, self.executable_path)
        if not os.path.exists(exe_path):
            print("WGPU executable not found, building...")
            if not build_wgpu():
                raise RuntimeError("Failed to build WGPU executable")
            print("Build completed.")
        
    def run_experiment(self, N):
        """Run WGPU experiment with given N and return average time in ms"""
        try:
            exe_path = os.path.join(self.base_dir, self.executable_path)
            result = subprocess.run(
                [exe_path, str(N)], 
                capture_output=True, 
                text=True
            )
            if result.returncode != 0:
                raise RuntimeError(f"WGPU execution failed: {result.stderr}")
            return int(result.stdout.strip())
        except Exception as e:
            raise RuntimeError(f"Failed to run WGPU benchmark: {e}")

def main():
    benchmark = WGPUBenchmark()
    benchmark.ensure_built()
    
    # Test sizes
    test_sizes = [10000000]
    
    print("N\tWGPU Time (ms)")
    print("-" * 20)
    
    for N in test_sizes:
        try:
            avg_time = benchmark.run_experiment(N)
            print(f"{N}\t{avg_time}")
        except RuntimeError as e:
            print(f"{N}\tERROR: {e}")

if __name__ == "__main__":
    main()