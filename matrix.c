#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
#include <time.h>
#include <math.h>

#define MATRIXSIZE 1000
#define DEBUG 0  // Ubah ke 1 jika ingin cek hasil (HANYA UNTUK MATRIX KECIL)

void printarr(float* arr, int n){
    fprintf(stdout, "\n");
    for(int row = 0; row < n*n; row++){
        if(row % n == 0 && row != 0) fprintf(stdout, "\n");
        fprintf(stdout, "%6.2f ", arr[row]);
    }
    fprintf(stdout, "\n\n");
}

int main(int argc, char **argv) {

    int comm_sz;
    int my_rank;
    int n = MATRIXSIZE;
    int master = 0;
    int tag = 0;
    double start_time, finish_time, final_time;

    // Ambil input ukuran matrix dari argumen CLI
    if (argc > 1) n = strtol(argv[1], NULL, 10);

    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &comm_sz);
    MPI_Comm_rank(MPI_COMM_WORLD, &my_rank);

    int np = (int)pow(comm_sz, 0.5);
    
    // Validasi kuadrat sempurna
    if (np * np != comm_sz) {
        if (my_rank == master) fprintf(stderr, "Error: Jumlah proses (%d) harus kuadrat sempurna (1, 4, 9, 16...)\n", comm_sz);
        MPI_Finalize();
        return 0;
    }

    int nr = n/np;

    if(n % np != 0){
        if(my_rank == master) fprintf(stderr, "Error: N (%d) harus habis dibagi sqrt(P) (%d).\n", n, np);
        MPI_Finalize();
        return 0;
    }

    float *a = NULL;
    float *b = NULL;
    float *flat_a = NULL;
    float *flat_b = NULL;

    if (my_rank == master) {
        a = (float *)malloc(n * n * sizeof(float));
        b = (float *)malloc(n * n * sizeof(float));
        flat_a = (float *)malloc(n * n * sizeof(float));
        flat_b = (float *)malloc(n * n * sizeof(float));

        srand(time(NULL));
        for (int i = 0; i < n*n; i++) {
            a[i] = (float)rand()/RAND_MAX * 2.0 - 1.0;
            b[i] = (float)rand()/RAND_MAX * 2.0 - 1.0;
        }

        if(DEBUG) {
            printf("Matrix A (Master):\n"); printarr(a, n);
            printf("Matrix B (Master):\n"); printarr(b, n);
        }

        fprintf(stdout, "Size: %d x %d, Processes: %d\n", n, n, comm_sz);

        // Re-ordering Matrix A agar sesuai blok scatter
        int idx = 0;
        for(int row_blk = 0; row_blk < np; row_blk++){
            for(int col_blk = 0; col_blk < np; col_blk++){
                int start_k = col_blk * nr + row_blk * n * nr;
                for(int r = 0; r < nr; r++){
                    for(int c = 0; c < nr; c++){
                        flat_a[idx++] = a[start_k + r*n + c];
                    }
                }
            }
        }

        // Re-ordering Matrix B
        idx = 0;
        for(int row_blk = 0; row_blk < np; row_blk++){
            for(int col_blk = 0; col_blk < np; col_blk++){
                int start_k = col_blk * nr + row_blk * n * nr;
                for(int r = 0; r < nr; r++){
                    for(int c = 0; c < nr; c++){
                        flat_b[idx++] = b[start_k + r*n + c];
                    }
                }
            }
        }
    }

    float *rank_a = (float *)malloc(nr * nr * sizeof(float));
    float *rank_b = (float *)malloc(nr * nr * sizeof(float));
    float *local_a = (float *)malloc(nr * nr * sizeof(float));
    float *local_b = (float *)malloc(nr * nr * sizeof(float));
    float *result = (float *)malloc(nr * nr * sizeof(float));

    // Inisialisasi result dengan 0
    for(int i=0; i<nr*nr; i++) result[i] = 0.0;

    MPI_Scatter(flat_a, nr*nr, MPI_FLOAT, rank_a, nr*nr, MPI_FLOAT, 0, MPI_COMM_WORLD);
    MPI_Scatter(flat_b, nr*nr, MPI_FLOAT, rank_b, nr*nr, MPI_FLOAT, 0, MPI_COMM_WORLD);

    start_time = MPI_Wtime();

    // Setup Grid Source
    int source[np*np];
    for(int i = 0; i < np; ++i) source[i] = i*(np+1);
    for(int i = 1; i < np; ++i){
        for(int j = 0; j < np; ++j){
            if((source[(i-1)*np+j] + 1) >= np*(j+1)) source[i*np+j]=np*(j);
            else source[i*np+j]=source[(i-1)*np+j] + 1;
        }
    }

    MPI_Status status;
    
    // --- FIX 2: Gunakan request terpisah untuk send dan recv agar aman ---
    MPI_Request req_send, req_recv; 

    for(int i = 0; i < np; i++){
        for(int j = 0; j < np; j++){
            // Copy rank_b ke local_b
            for(int k=0; k<nr*nr; k++) local_b[k] = rank_b[k];

            int low = (source[i*np+j]/np) * np;
            int high = low + np;

            // Broadcast A secara manual di baris (Simplifikasi Fox)
            if(my_rank == source[i*np+j]){
                for(int k = low; k < high; k++){
                    if(my_rank != k){
                        MPI_Send(rank_a, nr*nr, MPI_FLOAT, k, tag, MPI_COMM_WORLD);
                    } else {
                        for(int l=0; l<nr*nr; l++) local_a[l] = rank_a[l];
                    }
                }
            } else {
                if(my_rank >= low && my_rank < high){
                    MPI_Recv(local_a, nr*nr, MPI_FLOAT, source[i*np+j], tag, MPI_COMM_WORLD, &status);
                }
            }

            // Matrix Multiplication Kernel
            for (int x = 0; x < nr; x++) {
                for (int y = 0; y < nr; y++) {
                    float sum = 0.0;
                    for (int z = 0; z < nr ; z++) {
                        sum += local_a[x*nr+z] * local_b[z*nr+y];
                    }
                    result[x*nr+y] += sum;
                }
            }
        }

        // Shift B ke atas
        int destination = my_rank - np;
        int src = my_rank + np;
        if (destination < 0) destination += np*np;
        if (src >= np*np) src -= np*np;

        MPI_Barrier(MPI_COMM_WORLD);
        
        // --- FIX 2: Non-blocking Send dan Recv yang aman ---
        // Kirim 'rank_b' milik kita ke atas (destination)
        MPI_Isend(rank_b, nr*nr, MPI_FLOAT, destination, 0, MPI_COMM_WORLD, &req_send);
        
        // Terima 'rank_b' baru dari bawah (src) ke buffer sementara 'local_b'
        // Kita pakai local_b sebagai buffer terima sementara agar rank_b tidak tertimpa saat masih dikirim
        MPI_Irecv(local_b, nr*nr, MPI_FLOAT, src, 0, MPI_COMM_WORLD, &req_recv);
        
        // Tunggu keduanya selesai
        MPI_Wait(&req_send, &status);
        MPI_Wait(&req_recv, &status);
        
        // Pindahkan local_b (yang baru diterima) kembali ke rank_b untuk iterasi selanjutnya
        for(int k=0; k<nr*nr; k++) rank_b[k] = local_b[k];
    }

    finish_time = MPI_Wtime();
    final_time = finish_time - start_time;

    if(my_rank == master) {
        printf("Total Time Elapsed is %.6f seconds\n", final_time);
    }

    // --- FIX 1: Masalah Segfault disini ---
    // Hanya lakukan Gather jika DEBUG dinyalakan
    if (DEBUG) {
        float *final_matrix = NULL;
        if (my_rank == master) {
            final_matrix = (float *)malloc(n * n * sizeof(float));
        }

        // Semua proses harus memanggil ini jika masuk blok DEBUG
        MPI_Gather(result, nr*nr, MPI_FLOAT, final_matrix, nr*nr, MPI_FLOAT, 0, MPI_COMM_WORLD);

        if(my_rank == master){
            printf("Result Matrix (Block Ordered Check):\n");
            printarr(final_matrix, n); // Hati-hati print matrix besar!
            free(final_matrix);
        }
    }

    // Cleanup Memory
    free(rank_a); free(rank_b); free(local_a); free(local_b); free(result);
    if(my_rank == master) {
        free(a); free(b); free(flat_a); free(flat_b);
    }

    MPI_Finalize();
    return 0;
}