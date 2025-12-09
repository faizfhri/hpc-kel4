"""
Docker Management Utilities
Handle Docker container operations for the HPC cluster
"""

import docker
import logging
from typing import List, Dict, Optional
import time

logger = logging.getLogger(__name__)


class DockerManager:
    """Manages Docker containers for the MPI cluster"""
    
    def __init__(self):
        """Initialize Docker client"""
        try:
            self.client = docker.from_env()
            self.network_name = "mpi-net"
            self.volume_name = "mpi_home"
            self.image_name = "mpi-node"
        except Exception as e:
            logger.error(f"Failed to initialize Docker client: {e}")
            self.client = None
    
    def is_docker_available(self) -> bool:
        """Check if Docker is available and running"""
        if self.client is None:
            return False
        try:
            self.client.ping()
            return True
        except Exception as e:
            logger.error(f"Docker not available: {e}")
            return False
    
    def get_cluster_status(self) -> Dict[str, str]:
        """Get status of all cluster nodes"""
        nodes = ["hpchead", "node01", "node02", "node03"]
        status = {}
        
        if not self.is_docker_available():
            return {node: "docker_unavailable" for node in nodes}
        
        for node in nodes:
            try:
                container = self.client.containers.get(node)
                status[node] = container.status
            except docker.errors.NotFound:
                status[node] = "not_found"
            except Exception as e:
                logger.error(f"Error getting status for {node}: {e}")
                status[node] = "error"
        
        return status
    
    def start_cluster(self, num_nodes: int = 4) -> Dict[str, bool]:
        """Start the MPI cluster with specified number of nodes"""
        results = {}
        
        if not self.is_docker_available():
            return {"error": False, "message": "Docker is not available"}
        
        # Ensure network exists
        self._ensure_network()
        
        # Ensure volume exists
        self._ensure_volume()
        
        # Start head node
        results["hpchead"] = self._start_container("hpchead")
        time.sleep(2)  # Give head node time to initialize
        
        # Start worker nodes
        for i in range(1, num_nodes):
            node_name = f"node{i:02d}"
            results[node_name] = self._start_container(node_name)
            time.sleep(1)
        
        return results
    
    def stop_cluster(self) -> Dict[str, bool]:
        """Stop all cluster nodes"""
        nodes = ["hpchead", "node01", "node02", "node03"]
        results = {}
        
        for node in nodes:
            try:
                container = self.client.containers.get(node)
                container.stop()
                container.remove()
                results[node] = True
            except docker.errors.NotFound:
                results[node] = True  # Already stopped
            except Exception as e:
                logger.error(f"Error stopping {node}: {e}")
                results[node] = False
        
        return results
    
    def _ensure_network(self):
        """Ensure Docker network exists"""
        try:
            self.client.networks.get(self.network_name)
        except docker.errors.NotFound:
            self.client.networks.create(self.network_name, driver="bridge")
            logger.info(f"Created network: {self.network_name}")
    
    def _ensure_volume(self):
        """Ensure Docker volume exists"""
        try:
            self.client.volumes.get(self.volume_name)
        except docker.errors.NotFound:
            self.client.volumes.create(self.volume_name)
            logger.info(f"Created volume: {self.volume_name}")
    
    def _start_container(self, name: str) -> bool:
        """Start a single container"""
        try:
            # Check if container already exists
            try:
                container = self.client.containers.get(name)
                if container.status == "running":
                    logger.info(f"Container {name} already running")
                    return True
                else:
                    container.start()
                    logger.info(f"Started existing container: {name}")
                    return True
            except docker.errors.NotFound:
                # Create new container
                container = self.client.containers.run(
                    self.image_name,
                    name=name,
                    hostname=name,
                    network=self.network_name,
                    volumes={self.volume_name: {'bind': '/home/faiz', 'mode': 'rw'}},
                    detach=True,
                    remove=False,
                    tty=True
                )
                logger.info(f"Created and started new container: {name}")
                return True
        except Exception as e:
            logger.error(f"Failed to start container {name}: {e}")
            return False
    
    def execute_command(self, container_name: str, command: str) -> tuple:
        """Execute a command in a container and return (exit_code, output)"""
        try:
            container = self.client.containers.get(container_name)
            # Run as user 'faiz' to ensure SSH keys are accessible
            exec_cmd = f"su - faiz -c '{command}'"
            exit_code, output = container.exec_run(exec_cmd)
            return exit_code, output.decode('utf-8')
        except Exception as e:
            logger.error(f"Failed to execute command in {container_name}: {e}")
            return -1, str(e)
    
    def get_container_stats(self, container_name: str) -> Optional[Dict]:
        """Get resource usage stats for a container"""
        try:
            container = self.client.containers.get(container_name)
            stats = container.stats(stream=False)
            return stats
        except Exception as e:
            logger.error(f"Failed to get stats for {container_name}: {e}")
            return None
    
    def copy_file_to_container(self, container_name: str, src_path: str, dst_path: str) -> bool:
        """Copy a file from host to container"""
        try:
            container = self.client.containers.get(container_name)
            with open(src_path, 'rb') as f:
                data = f.read()
            container.put_archive(dst_path, data)
            return True
        except Exception as e:
            logger.error(f"Failed to copy file to {container_name}: {e}")
            return False
    
    def get_logs(self, container_name: str, tail: int = 100) -> str:
        """Get logs from a container"""
        try:
            container = self.client.containers.get(container_name)
            logs = container.logs(tail=tail).decode('utf-8')
            return logs
        except Exception as e:
            logger.error(f"Failed to get logs from {container_name}: {e}")
            return f"Error: {e}"
