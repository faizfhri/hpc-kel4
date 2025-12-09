#!/bin/bash

# --- KONFIGURASI ---
OUTPUT_FILE="hasil_benchmark.csv"
SIZES=(100 500 1000 1500 2000) # Ukuran matriks yang diuji
NP=4                           # Total proses (Wajib kuadrat sempurna: 4)

# --- PERSIAPAN ---
echo "1. Menyiapkan Hostfile untuk Multi-Node..."
# Kita buat hostfile baru agar yakin isinya benar
echo "hpchead" > hostfile_multi
echo "node01" >> hostfile_multi
echo "node02" >> hostfile_multi
echo "node03" >> hostfile_multi

echo "2. Compile ulang source code..."
# Compile Serial
if [ -f "serial.c" ]; then
    gcc serial.c -o serial_matrix
else
    echo "Error: File serial.c tidak ditemukan!"
    exit 1
fi

# Compile MPI
if [ -f "matrix.c" ]; then
    mpicc matrix.c -o matrix_mul -lm
else
    echo "Error: File matrix.c tidak ditemukan!"
    exit 1
fi

# Header CSV
echo "Matrix_Size,Serial_Time,MPI_SingleNode_Time,MPI_MultiNode_Time" > $OUTPUT_FILE

# Cetak Header Tabel ke Layar
echo ""
echo "============================================================================"
echo "           BENCHMARKING: SERIAL vs SINGLE NODE vs MULTI NODE                "
echo "============================================================================"
printf "| %-6s | %-12s | %-18s | %-18s |\n" "SIZE" "SERIAL (s)" "MPI SINGLE (s)" "MPI MULTI (s)"
echo "|--------|--------------|--------------------|--------------------|"

# --- LOOP PENGUJIAN ---
for N in "${SIZES[@]}"
do
    # A. JALANKAN SERIAL
    # Mengambil angka waktu dari output serial
    T_SERIAL=$(./serial_matrix $N | grep "Total Time" | awk '{print $5}')
    if [ -z "$T_SERIAL" ]; then T_SERIAL="Err"; fi


    # B. JALANKAN MPI SINGLE NODE (Multicore simulation)
    # Fix: Tambah "2> /dev/null" untuk membuang warning SSH
    T_SINGLE=$(mpirun -np $NP ./matrix_mul $N 2> /dev/null | grep "Total Time" | awk '{print $5}')
    if [ -z "$T_SINGLE" ]; then T_SINGLE="Err"; fi


    # C. JALANKAN MPI MULTI NODE (Distributed Cluster)
    # Fix: Tambah "2> /dev/null" untuk membuang warning SSH
    T_MULTI=$(mpirun -f hostfile_multi -np $NP ./matrix_mul $N 2> /dev/null | grep "Total Time" | awk '{print $5}')
    if [ -z "$T_MULTI" ]; then T_MULTI="Err"; fi


    # Simpan ke CSV
    echo "$N,$T_SERIAL,$T_SINGLE,$T_MULTI" >> $OUTPUT_FILE

    # Tampilkan ke Layar
    printf "| %-6d | %-12s | %-18s | %-18s |\n" "$N" "$T_SERIAL" "$T_SINGLE" "$T_MULTI"

done

echo "============================================================================"
echo "Selesai! Hasil lengkap tersimpan di: $OUTPUT_FILE"