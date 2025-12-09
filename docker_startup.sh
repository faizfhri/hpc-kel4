#!/bin/bash
# Startup script untuk initialize SSH di container

# Setup SSH directory
mkdir -p /home/faiz/.ssh
chmod 700 /home/faiz/.ssh

# Copy pre-generated SSH keys from template (same keys for all nodes)
cp /root/.ssh_template/id_rsa /home/faiz/.ssh/id_rsa
cp /root/.ssh_template/id_rsa.pub /home/faiz/.ssh/id_rsa.pub
cp /root/.ssh_template/authorized_keys /home/faiz/.ssh/authorized_keys
cp /root/.ssh_template/config /home/faiz/.ssh/config

# Set correct permissions
chmod 600 /home/faiz/.ssh/id_rsa
chmod 644 /home/faiz/.ssh/id_rsa.pub
chmod 600 /home/faiz/.ssh/authorized_keys
chmod 600 /home/faiz/.ssh/config
chown -R faiz:faiz /home/faiz/.ssh

# Start SSH daemon
exec /usr/sbin/sshd -D
