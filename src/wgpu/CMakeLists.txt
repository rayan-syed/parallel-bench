cmake_minimum_required(VERSION 3.0...3.25)
project(
    PARALLEL_BENCH
    VERSION 0.1.0
    LANGUAGES CXX C
)

add_executable( 
    wgpu
    src/main.cpp
    src/webgpu_utils.cpp
    src/shaders/shader.cpp
)

set_target_properties(wgpu PROPERTIES
    CXX_STANDARD 17
    CXX_STANDARD_REQUIRED ON
    CXX_EXTENSIONS OFF
    COMPILE_WARNING_AS_ERROR ON
)

if (MSVC)
    target_compile_options(wgpu PRIVATE /W4)
else()
    target_compile_options(wgpu PRIVATE -Wall -Wextra -pedantic)
endif()

# Include WebGPU subdirectory
add_subdirectory(webgpu)

# Link WebGPU library to wgpu_dft
target_link_libraries(wgpu PRIVATE webgpu)

# Copy necessary runtime binaries
target_copy_webgpu_binaries(wgpu)