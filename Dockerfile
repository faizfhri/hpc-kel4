FROM debian:latest

# 1. Install SSH, GCC (Compiler), dan MPICH (Library MPI)
RUN apt-get update && apt-get install -y \
    ssh \
    build-essential \
    mpich \
    iproute2 \
    iputils-ping \
    nano \
    && apt-get clean

# 2. Setup Folder Privilege Separation untuk SSH
# (FIX: Pakai -p agar tidak error jika folder sudah ada)
RUN mkdir -p /run/sshd

# 3. Buat User 'faiz'
RUN useradd faiz --uid=11000 -m -s /bin/bash
RUN echo "faiz:faiz123" | chpasswd

# 4. Set working directory
WORKDIR /home/faiz

# 5. Jalankan SSH Daemon saat container start
CMD ["/usr/sbin/sshd", "-D"]