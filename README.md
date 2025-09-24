# Benchmarking Parallel Processing Approaches on CPUs

The goal of this repo is to explore different parallel processing approaches on CPUs and understand their pros/cons.

## Motivation

There are many ways to run multi-threaded processes on CPUs. Through recent other proejcts I've found that even GPU-focused software can be run on CPUs via simulation (ex. WebGPU). I was curious as to the difference in the runtimes of something like that vs. something built for CPU parallel processing (ex. FastFlow, OpenMP). I believe WebGPU utilizes SwiftShader in its backend as well so any benchmarking on WebGPU here will probably be replaced with SwiftShader soon.