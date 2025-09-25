#ifndef SHADER_H
#define SHADER_H
#include <fstream>
#include <sstream>
#include <cmath>
#include <vector>
#include <chrono>
#include <webgpu/webgpu.hpp>
#include "../webgpu_utils.h"

long shader(
    WebGPUContext& context, 
    wgpu::Buffer& outputBuffer, 
    wgpu::Buffer& inputBuffer1, 
    wgpu::Buffer& inputBuffer2,
    size_t bufferlen
);

#endif 
