#define WEBGPU_CPP_IMPLEMENTATION
#include <iostream>
#include <vector>
#include <random>
#include <chrono>
#include <algorithm>
#include "webgpu_utils.h"
#include "mult/mult.h"

using namespace std;

int main() {
    // init wgpu
    WebGPUContext context;
    initWebGPU(context);

    // input vectors
    const int N = 10000000;
    mt19937 gen(random_device{}());
    uniform_real_distribution<> dist(0, 100);
    vector<float> A(N), B(N);
    for (int i = 0; i < N; i++) A[i] = dist(gen), B[i] = dist(gen);

    // transfer to gpu
    wgpu::Buffer ABuffer = createBuffer(context.device, A.data(), sizeof(float) * N, wgpu::BufferUsage::Storage);
    wgpu::Buffer BBuffer = createBuffer(context.device, B.data(), sizeof(float) * N, wgpu::BufferUsage::Storage);

    // output buffer
    wgpu::Buffer outputBuffer = createBuffer(context.device, nullptr, sizeof(float) * N, WGPUBufferUsage(wgpu::BufferUsage::Storage | wgpu::BufferUsage::CopySrc));

    // multiply and track durations
    int runs = 10;
    int duration = 0;
    for(int i = 0; i<runs; i++) {
        auto start = chrono::high_resolution_clock::now();
        mult(context, outputBuffer, ABuffer, BBuffer, N);
        auto end = chrono::high_resolution_clock::now();
        duration += chrono::duration_cast<chrono::milliseconds>(end - start).count();
    }
    duration /= runs;

    cout << "Average time elapsed with wgpu: " << duration << endl;

    ABuffer.release();
    BBuffer.release();
    outputBuffer.release();

    // transform
    vector<float> out(N);
    runs = 10;
    duration = 0;
    for(int i = 0; i<runs; i++) {
        auto start = chrono::high_resolution_clock::now();
        transform(A.begin(), A.end(), B.begin(), out.begin(), [](float x, float y) { return x * y; });
        auto end = chrono::high_resolution_clock::now();
        duration += chrono::duration_cast<chrono::milliseconds>(end - start).count();
    }
    duration /= runs;

    cout << "Average time elapsed with transform: " << duration << endl;
    return 0;
}