#!/bin/bash
# Script untuk setup SSH keys di semua nodes setelah cluster start

echo "Setting up SSH keys across cluster..."

# Generate SSH key di hpchead jika belum ada
docker exec hpchead su - faiz -c "
if [ ! -f ~/.ssh/id_rsa ]; then
    mkdir -p ~/.ssh
    ssh-keygen -t rsa -f ~/.ssh/id_rsa -N ''
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
    chmod 600 ~/.ssh/authorized_keys
    chmod 700 ~/.ssh
fi

# Configure SSH client
cat > ~/.ssh/config <<EOF
Host *
    StrictHostKeyChecking no
    UserKnownHostsFile=/dev/null
    LogLevel ERROR
EOF
chmod 600 ~/.ssh/config
"

# Copy SSH directory ke semua worker nodes
for node in node01 node02 node03; do
    echo "Copying SSH keys to $node..."
    
    docker exec $node su - faiz -c "
    mkdir -p ~/.ssh
    chmod 700 ~/.ssh
    "
    
    # Copy from shared volume
    docker exec hpchead su - faiz -c "
    if [ -f ~/.ssh/id_rsa ]; then
        cp ~/.ssh/id_rsa /tmp/id_rsa_temp
        cp ~/.ssh/id_rsa.pub /tmp/id_rsa_pub_temp
        cp ~/.ssh/authorized_keys /tmp/authorized_keys_temp
        cp ~/.ssh/config /tmp/config_temp
    fi
    "
    
    docker exec $node su - faiz -c "
    cp /tmp/id_rsa_temp ~/.ssh/id_rsa
    cp /tmp/id_rsa_pub_temp ~/.ssh/id_rsa.pub
    cp /tmp/authorized_keys_temp ~/.ssh/authorized_keys
    cp /tmp/config_temp ~/.ssh/config
    chmod 600 ~/.ssh/id_rsa
    chmod 644 ~/.ssh/id_rsa.pub
    chmod 600 ~/.ssh/authorized_keys
    chmod 600 ~/.ssh/config
    "
done

# Test SSH connections
echo ""
echo "Testing SSH connections..."
docker exec hpchead su - faiz -c "
for node in hpchead node01 node02 node03; do
    echo -n \"Testing \$node: \"
    ssh \$node 'echo OK' 2>/dev/null || echo 'FAILED'
done
"

echo ""
echo "SSH setup complete!"
