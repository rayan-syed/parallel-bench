#include <iostream>
#include <vector>
#include <random>
#include <chrono>
#ifdef _OPENMP
  #include <omp.h>
#endif

using namespace std;

int main(int argc, char** argv) {
    if (argc != 2) {
        cerr << "Usage: " << argv[0] << " <N>" << endl;
        return 1;
    }
    
    int N = atoi(argv[1]);
    if (N <= 0) {
        cerr << "N must be positive" << endl;
        return 1;
    }

    // generate input vectors
    mt19937 gen(random_device{}());
    uniform_real_distribution<> dist(0, 100);
    vector<float> A(N), B(N), out(N);
    for (int i = 0; i < N; i++) A[i] = dist(gen), B[i] = dist(gen);

    for (int i = 0; i < N; ++i) {
        A[i] = dist(gen);
        B[i] = dist(gen);
    }

    // warmup
    #pragma omp parallel for
    for (int i = 0; i < N; ++i) out[i] = A[i] * B[i];

    // benchmark
    const int runs = 10;
    long total_ms = 0;
    for (int r = 0; r < runs; r++) {
        auto start = chrono::high_resolution_clock::now();
        #pragma omp parallel for
        for (int i = 0; i < N; i++) {
            out[i] = A[i] * B[i];
        }
        auto end = chrono::high_resolution_clock::now();
        total_ms += chrono::duration_cast<chrono::milliseconds>(end - start).count();
    }

    long avg_ms = total_ms / runs;
    cout << avg_ms << endl; 
    return 0;
}
