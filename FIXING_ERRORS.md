# Fixing Errors - Rebuild Required

Setelah update Dockerfile dan docker-compose.yml, Anda perlu rebuild Docker images dan restart cluster.

## Steps to Fix

### 1. Stop dan Remove Existing Containers

```bash
# Stop semua container yang running
docker-compose down

# Remove containers (optional, untuk clean slate)
docker rm hpchead node01 node02 node03

# Remove old image (optional)
docker rmi mpi-node
```

### 2. Rebuild Docker Image

```bash
# Build ulang image dengan konfigurasi baru
docker-compose build --no-cache

# Atau build manual:
docker build -t mpi-node .
```

### 3. Start Cluster dengan Konfigurasi Baru

```bash
# Start cluster dengan docker-compose (dengan shm_size baru)
docker-compose up -d

# Verify containers running
docker ps

# Check logs jika ada masalah
docker-compose logs
```

### 4. Test SSH Connection (Manual Verification)

```bash
# Masuk ke head node
docker exec -it hpchead bash

# Switch ke user faiz
su - faiz

# Test SSH ke worker nodes (seharusnya tidak minta password)
ssh node01 hostname
ssh node02 hostname
ssh node03 hostname

# Test MPI hello world
echo "hpchead
node01
node02
node03" > hostfile

mpirun -np 4 --hostfile hostfile hostname

# Exit
exit
exit
```

## What Was Fixed?

### 1. Multi-Node SSH Error (Host Key Verification)
**Before:**
```
Host key verification failed.
[mpiexec@hpchead] ui_cmd_cb: Launch proxy failed
```

**Fixed by:**
- Added SSH key generation in Dockerfile
- Configured `StrictHostKeyChecking no` 
- Set `UserKnownHostsFile=/dev/null`
- Properly setup authorized_keys

### 2. Shared Memory Error (16 Processes)
**Before:**
```
UCX ERROR Not enough memory to write total of 4292720 bytes
Please check that /dev/shm has more available memory
```

**Fixed by:**
- Added `shm_size: 512m` to all containers in docker-compose.yml
- Default Docker shm is only 64MB, now 512MB per container
- Total 2GB shared memory across 4 nodes

### 3. User-Friendly Error Messages
**Before:**
- Errors hanya di raw_output
- Tidak jelas apa masalahnya

**Fixed by:**
- Parse common errors dan tampilkan pesan user-friendly
- Separate "Technical Details" expander untuk raw errors
- Validation warnings untuk process count

## Troubleshooting

### Image Build Failed
```bash
# Check Docker logs
docker-compose logs

# Try manual build with verbose output
docker build -t mpi-node . --progress=plain
```

### Containers Won't Start
```bash
# Check container logs
docker logs hpchead
docker logs node01

# Check if ports are occupied
docker ps -a

# Force remove and restart
docker-compose down -v
docker-compose up -d
```

### Still Getting SSH Errors
```bash
# Rebuild image without cache
docker-compose build --no-cache

# Remove all MPI containers and volumes
docker-compose down -v
docker volume rm mpi_home

# Start fresh
docker-compose up -d
```

### Memory Still Insufficient
```bash
# Edit docker-compose.yml and increase shm_size
# Change from 512m to 1g or 2g

shm_size: 1g  # or 2g

# Then restart
docker-compose down
docker-compose up -d
```

## Quick Commands

```bash
# Complete reset and rebuild
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
docker ps

# Check if MPI works
docker exec -it hpchead su - faiz -c "mpirun -np 4 --host hpchead:1,node01:1,node02:1,node03:1 hostname"
```

## Verification Checklist

- [ ] Docker image rebuilt successfully
- [ ] All 4 containers running (`docker ps`)
- [ ] SSH works without password prompt
- [ ] MPI hello world works across nodes
- [ ] Streamlit app can detect running cluster
- [ ] Single node benchmark works (4 processes)
- [ ] Multi node benchmark works (4 processes)
- [ ] No memory errors with 8 processes

## Next Steps

1. Rebuild menggunakan commands di atas
2. Start Streamlit: `streamlit run app.py`
3. Go to Overview page dan verify semua nodes running
4. Test benchmark dengan 4 processes
5. Jika berhasil, coba test dengan 8 processes
6. Jika masih error, check logs dan troubleshoot
