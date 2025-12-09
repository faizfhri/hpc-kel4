#!/bin/bash
# One-time setup script to generate shared SSH key

echo "Generating shared SSH key for MPI cluster..."

# Create temporary directory
mkdir -p .ssh_temp
cd .ssh_temp

# Generate SSH key
ssh-keygen -t rsa -f id_rsa -N '' -C "mpi-cluster"

# Create authorized_keys
cat id_rsa.pub > authorized_keys

# Create SSH config
cat > config <<EOF
Host *
    StrictHostKeyChecking no
    UserKnownHostsFile=/dev/null
    LogLevel ERROR
EOF

echo ""
echo "SSH keys generated in .ssh_temp/"
echo "These will be copied into Docker image during build"
ls -la

cd ..
