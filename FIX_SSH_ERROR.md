# Quick Fix untuk Multi-Node SSH Error

## Problem
```
Host key verification failed.
[mpiexec@hpchead] ui_cmd_cb: Launch proxy failed
```

## Root Cause
SSH keys tidak ter-sync antar containers karena volume mount.

## Solution
Rebuild Docker image dengan SSH keys yang di-embed di image (bukan di volume).

## Steps

### 1. Stop & Remove Containers
```bash
docker-compose down
docker rm -f hpchead node01 node02 node03 2>/dev/null || true
```

### 2. Rebuild Image
```bash
# Rebuild dengan no-cache untuk force regenerate SSH keys
docker-compose build --no-cache

# Atau manual build
docker build --no-cache -t mpi-node .
```

### 3. Start Cluster
```bash
docker-compose up -d
```

### 4. Verify SSH Works
```bash
# Test SSH connectivity
docker exec -it hpchead su - faiz -c "
for node in hpchead node01 node02 node03; do
    echo -n 'Testing \$node: '
    ssh -o ConnectTimeout=5 \$node hostname 2>/dev/null && echo '✓ OK' || echo '✗ FAILED'
done
"
```

### 5. Test MPI
```bash
# Test MPI across all nodes
docker exec -it hpchead su - faiz -c "mpirun -np 4 --host hpchead,node01,node02,node03 hostname"
```

**Expected output:**
```
hpchead
node01
node02
node03
```

## How It Works Now

**Before (BROKEN):**
- SSH keys generated during Dockerfile build
- Volume mounted to `/home/faiz` overwrites SSH keys
- Each container has different keys → authentication fails

**After (FIXED):**
- SSH keys generated and stored in `/root/.ssh_template` during build
- Startup script copies keys to `/home/faiz/.ssh` when container starts
- All containers use SAME SSH keys → authentication works
- Keys survive volume mounts

## Troubleshooting

### Still Getting SSH Errors?

```bash
# Check if SSH keys exist in container
docker exec hpchead ls -la /home/faiz/.ssh/

# Should show:
# -rw-------  id_rsa
# -rw-r--r--  id_rsa.pub
# -rw-------  authorized_keys
# -rw-------  config

# Check SSH config
docker exec hpchead cat /home/faiz/.ssh/config

# Should contain:
# StrictHostKeyChecking no
# UserKnownHostsFile=/dev/null
```

### Manual Fix Inside Container

```bash
# If keys are missing, manually copy from template
docker exec hpchead bash -c "
cp /root/.ssh_template/* /home/faiz/.ssh/
chown -R faiz:faiz /home/faiz/.ssh
chmod 600 /home/faiz/.ssh/id_rsa
chmod 600 /home/faiz/.ssh/authorized_keys
chmod 600 /home/faiz/.ssh/config
"

# Repeat for all nodes
for node in node01 node02 node03; do
    docker exec $node bash -c "
    cp /root/.ssh_template/* /home/faiz/.ssh/
    chown -R faiz:faiz /home/faiz/.ssh
    chmod 600 /home/faiz/.ssh/id_rsa
    chmod 600 /home/faiz/.ssh/authorized_keys
    chmod 600 /home/faiz/.ssh/config
    "
done
```

## Complete Rebuild Command

```bash
# One-liner untuk complete reset dan rebuild
docker-compose down && \
docker rm -f hpchead node01 node02 node03 2>/dev/null; \
docker-compose build --no-cache && \
docker-compose up -d && \
sleep 5 && \
docker exec -it hpchead su - faiz -c "mpirun -np 4 --host hpchead,node01,node02,node03 hostname"
```

## Next Steps After Fix

1. ✅ Verify MPI works: `mpirun -np 4 --host ... hostname`
2. ✅ Compile code: `mpicc -o matrix matrix.c -lm`
3. ✅ Test single node: `mpirun -np 4 --host hpchead ./matrix 500`
4. ✅ Test multi node: `mpirun -np 4 --host hpchead,node01,node02,node03 ./matrix 500`
5. ✅ Run Streamlit and test via UI

## Key Files Changed

- `Dockerfile`: SSH keys embedded in `/root/.ssh_template`
- `docker_startup.sh`: Startup script copies keys to `/home/faiz/.ssh`
- `docker-compose.yml`: Added `shm_size: 512m` for memory

All containers now start with identical SSH configuration!
