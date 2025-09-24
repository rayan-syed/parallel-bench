"""
Top-level orchestrator for parallel-bench.
Runs benchmarks across frameworks and saves results.
"""

from src.runners.wgpu_runner import WGPURunner

def main():
    runner = WGPURunner()
    runner.build()

    sizes = [1_000_000, 5_000_000, 10_000_000, 20_000_000]
    print(f"{'N':>12} | {'WGPU (ms)':>12}")
    print("-" * 27)
    for N in sizes:
        avg_time = runner.run(N)
        print(f"{N:>12,d} | {avg_time:>12}")

if __name__ == "__main__":
    main()
