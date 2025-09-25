#define WEBGPU_CPP_IMPLEMENTATION
#include <iostream>
#include <vector>
#include <random>
#include <chrono>
#include <algorithm>
#include <execution>
#include <cstdlib>
#include "webgpu_utils.h"
#include "shaders/shader.h"

using namespace std;

int main(int argc, char* argv[]) {
    if (argc != 3) {
        cerr << "Usage: " << argv[0] << " <N> <shaderType>" << endl;
        return 1;
    }
    
    int N = atoi(argv[1]);
    int shaderType = atoi(argv[2]); // 0 = simple, 1 = complex

    if (N <= 0) {
        cerr << "N must be positive" << endl;
        return 1;
    }

    // init wgpu
    WebGPUContext context;
    initWebGPU(context);

    // generate input vectors
    mt19937 gen(random_device{}());
    uniform_real_distribution<> dist(0, 100);
    vector<float> A(N), B(N);
    for (int i = 0; i < N; i++) A[i] = dist(gen), B[i] = dist(gen);

    // transfer to gpu
    wgpu::Buffer ABuffer = createBuffer(context.device, A.data(), sizeof(float) * N, wgpu::BufferUsage::Storage);
    wgpu::Buffer BBuffer = createBuffer(context.device, B.data(), sizeof(float) * N, wgpu::BufferUsage::Storage);

    // output buffer
    wgpu::Buffer outputBuffer = createBuffer(context.device, nullptr, sizeof(float) * N, WGPUBufferUsage(wgpu::BufferUsage::Storage | wgpu::BufferUsage::CopySrc));

    // warmup
    shader(context, outputBuffer, ABuffer, BBuffer, 100);

    // benchmark
    int runs = 10;
    long execution_ms = 0;
    long overhead_ms = 0;
    for(int r = 0; r < runs; r++) {
        auto start = chrono::high_resolution_clock::now();
        long execution = shader(context, outputBuffer, ABuffer, BBuffer, N, shaderType);
        auto end = chrono::high_resolution_clock::now();
        long duration = chrono::duration_cast<chrono::milliseconds>(end - start).count();
        execution_ms += execution;
        overhead_ms += (duration - execution);
    }
    long avg_execution_ms = execution_ms / runs;
    long avg_overhead_ms = overhead_ms / runs;
    long avg_total_ms = avg_execution_ms + avg_overhead_ms;

    cout << avg_execution_ms << " " << avg_overhead_ms << " " << avg_total_ms <<  endl; 

    ABuffer.release();
    BBuffer.release();
    outputBuffer.release();
    return 0;
}