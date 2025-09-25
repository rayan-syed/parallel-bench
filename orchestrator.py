"""
Top-level orchestrator for parallel-bench.
Runs benchmarks across frameworks and saves results.
"""

from src.runners.wgpu_runner import WGPURunner
from src.runners.omp_runner import OMPRunner

def main():
    sizes = [1_000_000, 5_000_000, 10_000_000]

    llvmpipe = WGPURunner(backend="llvmpipe")
    swiftshader = WGPURunner(backend="swiftshader")
    # omp = OMPRunner()

    llvmpipe.build()
    swiftshader.build()
    # omp.build()

    # header
    print("N,ShaderType,Backend,ExecMs,OverheadMs,TotalMs")

    # simple benchmarks
    for N in sizes:
        for backend, runner in [("llvmpipe", llvmpipe), ("swiftshader", swiftshader)]:
            exec_ms, over_ms, tot_ms = runner.run(N, shader_type=0)
            print(f"{N},simple,{backend},{exec_ms},{over_ms},{tot_ms}")

    # complex benchmarks
    for N in sizes:
        for backend, runner in [("llvmpipe", llvmpipe), ("swiftshader", swiftshader)]:
            exec_ms, over_ms, tot_ms = runner.run(N, shader_type=1)
            print(f"{N},complex,{backend},{exec_ms},{over_ms},{tot_ms}")

if __name__ == "__main__":
    main()