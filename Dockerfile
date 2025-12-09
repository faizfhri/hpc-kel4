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

# 4. Setup SSH keys (pre-generated for all nodes)
RUN mkdir -p /root/.ssh_template && \
    ssh-keygen -t rsa -f /root/.ssh_template/id_rsa -N '' && \
    cat /root/.ssh_template/id_rsa.pub >> /root/.ssh_template/authorized_keys && \
    echo "Host *" > /root/.ssh_template/config && \
    echo "    StrictHostKeyChecking no" >> /root/.ssh_template/config && \
    echo "    UserKnownHostsFile=/dev/null" >> /root/.ssh_template/config && \
    echo "    LogLevel ERROR" >> /root/.ssh_template/config && \
    chmod 600 /root/.ssh_template/id_rsa && \
    chmod 644 /root/.ssh_template/id_rsa.pub && \
    chmod 600 /root/.ssh_template/authorized_keys && \
    chmod 600 /root/.ssh_template/config

# 5. Copy startup script
COPY docker_startup.sh /usr/local/bin/docker_startup.sh
RUN chmod +x /usr/local/bin/docker_startup.sh

# 6. Set working directory
WORKDIR /home/faiz

# 7. Run startup script (will copy SSH keys and start daemon)
CMD ["/usr/local/bin/docker_startup.sh"]