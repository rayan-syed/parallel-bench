cmake_minimum_required(VERSION 3.15)
project(
    PARALLEL_BENCH
    VERSION 0.1.0
    LANGUAGES CXX C
)

find_package(OpenMP REQUIRED)

add_executable(
    omp_bench
    main.cpp
)

set_target_properties(omp_bench PROPERTIES
    CXX_STANDARD 17
    CXX_STANDARD_REQUIRED ON
    CXX_EXTENSIONS OFF
)

if (MSVC)
    target_compile_options(omp_bench PRIVATE /W4)
else()
    target_compile_options(omp_bench PRIVATE -Wall -Wextra -pedantic)
endif()

target_link_libraries(omp_bench PRIVATE OpenMP::OpenMP_CXX)
