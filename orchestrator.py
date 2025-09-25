"""
Top-level orchestrator for parallel-bench.
Runs benchmarks across frameworks and saves results + plots.
"""

from src.runners.wgpu_runner import WGPURunner
from src.runners.omp_runner import OMPRunner
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_lines(df, ycol, title_suffix, out_path):
    plt.figure(figsize=(6, 4))
    for backend in df["Backend"].unique():
        d = df[df["Backend"] == backend].sort_values("N")
        plt.plot(d["N"], d[ycol], marker="o", label=backend)
    plt.title(f"Benchmark ({title_suffix})")
    plt.xlabel("N (array size)")
    plt.ylabel(f"{ycol} (ms)")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()


def plot_stacked(df, shader_type, out_path):
    sub = df[df["ShaderType"] == shader_type]
    backends = sub["Backend"].unique()
    Ns = sorted(sub["N"].unique())

    bar_width = 0.25
    offsets = [(i - len(backends)/2) * bar_width for i in range(len(backends))]

    plt.figure(figsize=(8, 5))
    for offset, backend in zip(offsets, backends):
        d = sub[sub["Backend"] == backend].sort_values("N")
        x_positions = [n + offset for n in range(len(Ns))]

        plt.bar(
            x_positions,
            d["ExecMs"],
            width=bar_width,
            label=f"{backend} Exec"
        )
        plt.bar(
            x_positions,
            d["OverheadMs"],
            bottom=d["ExecMs"],
            width=bar_width,
            label=f"{backend} Overhead"
        )

    plt.xticks(range(len(Ns)), [f"{n:,}" for n in Ns])
    plt.xlabel("N (array size)")
    plt.ylabel("Time (ms)")
    plt.title(f"Benchmark ({shader_type}) — Exec + Overhead")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()


def main():
    # input sizes to test
    sizes = [1_000_000]

    # central list of backends/runners
    backends = [
        ("llvmpipe", WGPURunner(backend="llvmpipe")),
        ("swiftshader", WGPURunner(backend="swiftshader")),
        ("omp", OMPRunner()),
    ]

    # Build all
    for _, runner in backends:
        runner.build()

    results = []

    for shader_type in [("simple", 0), ("complex", 1)]:
        label, stype = shader_type
        print(f"Running {label} experiments...")
        for N in tqdm(sizes, desc=f"{label} experiments"):
            for backend, runner in backends:
                exec_ms, over_ms, tot_ms = runner.run(N, shader_type=stype)
                results.append({
                    "N": N,
                    "ShaderType": label,
                    "Backend": backend,
                    "ExecMs": exec_ms,
                    "OverheadMs": over_ms,
                    "TotalMs": tot_ms
                })

    # Save CSV
    os.makedirs("results", exist_ok=True)
    df = pd.DataFrame(results)
    csv_path = "results/bench.csv"
    df.to_csv(csv_path, index=False)
    print(f"Saved results to {csv_path}")

    # Plot
    for shader_type in df["ShaderType"].unique():
        sub = df[df["ShaderType"] == shader_type]

        plot_lines(sub, "TotalMs",
                   f"{shader_type} — Total time",
                   f"results/bench_{shader_type}_total.png")

        plot_stacked(sub,
                     shader_type,
                     f"results/bench_{shader_type}_stacked.png")

        print(f"Saved plots for {shader_type}")


if __name__ == "__main__":
    main()
