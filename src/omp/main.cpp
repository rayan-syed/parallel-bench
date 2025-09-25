#include <iostream>
#include <vector>
#include <random>
#include <chrono>
#include <cmath>
#include <cstdlib>
#ifdef _OPENMP
  #include <omp.h>
#endif

using namespace std;

int main(int argc, char** argv) {
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

    // generate input vectors
    mt19937 gen(random_device{}());
    uniform_real_distribution<> dist(0, 100);
    vector<float> A(N), B(N), out(N);
    for (int i = 0; i < N; i++) {
        A[i] = dist(gen);
        B[i] = dist(gen);
    }

    // warmup
    #pragma omp parallel for
    for (int i = 0; i < 100; ++i) {
        out[i] = A[i] * B[i];
    }

    // benchmark
    const int runs = 10;
    long total_ms = 0;
    for (int r = 0; r < runs; r++) {
        auto start = chrono::high_resolution_clock::now();

        #pragma omp parallel for
        for (int i = 0; i < N; i++) {
            float ai = A[i];
            float bi = B[i];
            float prod = ai * bi;
            // case simple
            if (shaderType == 0) {
                out[i] = prod;
            } 
            // case complex
            else {
                float v = prod + float(i) * 1e-4f + 1.0f;
                for (int outer = 0; outer < 128; ++outer) {
                    for (int inner = 0; inner < 16; ++inner) {
                        v = sin(v) + cos(v) * sqrt(fabs(v) + 1.0f);
                    }
                }
                if (v > 0.0f) {
                    out[i] = prod;
                } else {
                    out[i] = prod;
                }
            }
        }

        auto end = chrono::high_resolution_clock::now();
        total_ms += chrono::duration_cast<chrono::milliseconds>(end - start).count();
    }

    long avg_total_ms = total_ms / runs;
    long avg_exec_ms = avg_total_ms;
    long avg_overhead_ms = 0; // omp overhead nonexistent since runs natively on cpu

    cout << avg_exec_ms << " " << avg_overhead_ms << " " << avg_total_ms << endl;
    return 0;
}
