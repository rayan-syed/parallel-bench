# Benchmarking Parallel Processing Approaches on CPUs

This repository benchmarks different approaches to parallel processing on CPUs and examines their trade-offs.

## Motivation

There are many ways to exploit CPU parallelism. Traditional CPU-native frameworks (e.g. OpenMP, FastFlow) give explicit control over threads and scheduling. At the same time, GPU-oriented APIs such as WebGPU can still run on CPUs by using software rasterizers like llvmpipe (from Mesa) or SwiftShader (from Google). To experiment with GPU code on CPUs, WebGPU is used to change the runtimes.

The goal is not only to measure raw performance but also to understand the trade-offs:
- How do GPU-style runtimes (WebGPU + SwiftShader/llvmpipe) behave when emulated on CPUs?
- How close can they get to optimized CPU-native frameworks?
- What are the overheads and benefits of using a GPU-first programming model on a CPU?