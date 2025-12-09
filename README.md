MPI Cluster Simulation with Docker
Proyek ini adalah simulasi High Performance Computing (HPC) menggunakan Docker untuk membandingkan performa Matrix Multiplication secara Serial vs Parallel (MPI).

Prerequisites
Docker Installed

Cara Menjalankan (Step-by-Step)
1. Build Image & Network
Pertama, buat image Docker dan network bridge-nya.

Bash

docker build -t mpi-node .
docker network create mpi-net
docker volume create mpi_home
2. Jalankan Cluster (4 Node)
Jalankan perintah berikut di terminal (Host Machine) untuk menghidupkan 1 Head Node dan 3 Worker Nodes.

Head Node:

Bash

docker run -d --rm --name hpchead --hostname hpchead --network mpi-net -v mpi_home:/home/faiz mpi-node
Worker Nodes:

Bash

docker run -d --rm --name node01 --hostname node01 --network mpi-net -v mpi_home:/home/faiz mpi-node
docker run -d --rm --name node02 --hostname node02 --network mpi-net -v mpi_home:/home/faiz mpi-node
docker run -d --rm --name node03 --hostname node03 --network mpi-net -v mpi_home:/home/faiz mpi-node
3. Setup Permission & SSH
Lakukan konfigurasi awal agar node bisa saling komunikasi tanpa password.

Bash

# Masuk ke Head Node
docker exec -it hpchead su - faiz

# (Di dalam container hpchead)
# 1. Fix permission folder
sudo chown -R faiz:faiz /home/faiz

# 2. Generate SSH Key (Tekan Enter terus sampai selesai)
ssh-keygen -t rsa

# 3. Authorize Key & Config
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
echo -e "Host *\n\tStrictHostKeyChecking no\n\tUserKnownHostsFile /dev/null" > ~/.ssh/config
chmod 600 ~/.ssh/config
4. Jalankan Benchmark
Sekarang jalankan script otomatisasi untuk melihat perbandingan performa.

Bash

# Pastikan masih di dalam hpchead
chmod +x benchmark.sh
./benchmark.sh
Kenapa ini Keren?
Kalau kamu upload ini ke GitHub:

Portabilitas: Dosenmu bisa coba di Mac, Windows, atau Linux, hasilnya pasti sama.

Portfolio: Ini menunjukkan kamu mengerti Docker, Bash Scripting, dan Parallel Computing sekaligus.

Ada satu hal lagi: Karena kamu menulis file matrix.c dll di dalam container (lewat volume), file aslinya di laptop kamu mungkin ada di lokasi Docker Volume, bukan di folder mpi-cluster tempat kamu menyimpan Dockerfile.

Pastikan kamu copy file matrix.c, serial.c, dan benchmark.sh dari dalam container ke folder laptop sebelum git push!

Caranya (jalankan di terminal laptop):

Bash

# Copy dari container ke folder laptop saat ini
docker cp hpchead:/home/faiz/matrix.c .
docker cp hpchead:/home/faiz/serial.c .
docker cp hpchead:/home/faiz/benchmark.sh .
Setelah itu baru:

Bash

git init
git add .
git commit -m "Initial commit MPI Cluster"
git push origin main