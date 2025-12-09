#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Compile: gcc serial.c -o serial_matrix

int main(int argc, char **argv) {
    int n = 1000;
    if (argc > 1) n = atoi(argv[1]);

    float *a = (float *)malloc(n * n * sizeof(float));
    float *b = (float *)malloc(n * n * sizeof(float));
    float *res = (float *)malloc(n * n * sizeof(float));

    // Init dummy data
    for (int i = 0; i < n * n; i++) {
        a[i] = 1.0; b[i] = 1.0; res[i] = 0.0;
    }

    clock_t start = clock();

    // Matrix Multiplication O(N^3)
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            float sum = 0.0;
            for (int k = 0; k < n; k++) {
                sum += a[i * n + k] * b[k * n + j];
            }
            res[i * n + j] = sum;
        }
    }

    clock_t end = clock();
    double time_spent = (double)(end - start) / CLOCKS_PER_SEC;

    printf("Total Time Elapsed is %.6f seconds\n", time_spent);

    free(a); free(b); free(res);
    return 0;
}