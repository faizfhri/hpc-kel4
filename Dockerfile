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
RUN mkdir -p /run/sshd

# 3. Buat User 'faiz'
RUN useradd faiz --uid=11000 -m -s /bin/bash
RUN echo "faiz:faiz123" | chpasswd

# 4. Setup SSH untuk MPI tanpa password dan host key verification
RUN mkdir -p /home/faiz/.ssh && \
    ssh-keygen -t rsa -f /home/faiz/.ssh/id_rsa -N '' && \
    cat /home/faiz/.ssh/id_rsa.pub >> /home/faiz/.ssh/authorized_keys && \
    chmod 600 /home/faiz/.ssh/authorized_keys && \
    chmod 700 /home/faiz/.ssh && \
    chown -R faiz:faiz /home/faiz/.ssh

# 5. Configure SSH untuk skip host key verification
RUN echo "Host *" >> /home/faiz/.ssh/config && \
    echo "    StrictHostKeyChecking no" >> /home/faiz/.ssh/config && \
    echo "    UserKnownHostsFile=/dev/null" >> /home/faiz/.ssh/config && \
    chmod 600 /home/faiz/.ssh/config && \
    chown faiz:faiz /home/faiz/.ssh/config

# 6. Set working directory
WORKDIR /home/faiz

# 7. Jalankan SSH Daemon saat container start
CMD ["/usr/sbin/sshd", "-D"]