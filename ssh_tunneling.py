import subprocess
import time
import os

def terminate_existing_tunnels():
    """기존의 SSH 터널링을 모두 종료합니다"""
    result = subprocess.run(['pgrep', '-f', 'ssh -i'], stdout=subprocess.PIPE)
    pids = result.stdout.decode().strip().split('\n')
    for pid in pids:
        if pid:
            subprocess.run(['kill', '-9', pid])
    print("Existing SSH tunnels terminated.")

def create_ssh_tunnel(local_port, remote_host, remote_port, ssh_key_path, ssh_user, ssh_host, ssh_port, error_ports):
    command = [
        "ssh",
        "-i", ssh_key_path,
        "-L", f"{local_port}:{remote_host}:{remote_port}",
        "-p", str(ssh_port),
        "-N",
        "-f",
        f"{ssh_user}@{ssh_host}"
    ]
    try:
        print(f"Creating tunnel for local port {local_port} -> remote port {remote_port}")
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Tunnel created for local port {local_port} -> remote port {remote_port}")
    except subprocess.CalledProcessError as e:
        error_ports.append(local_port)
        print(f"Failed to create tunnel for local port {local_port}: {e.stderr.decode().strip()}")
    except Exception as e:
        error_ports.append(local_port)
        print(f"Unexpected error for local port {local_port}: {e}")

def create_tunnels_in_batches(start_port, end_port, batch_size, remote_host, ssh_key_path, ssh_user, ssh_host, ssh_port):
    error_ports = []
    for batch_start in range(start_port, end_port + 1, batch_size):
        batch_end = min(batch_start + batch_size - 1, end_port)
        print(f"Handling ports from {batch_start} to {batch_end}")
        for port in range(batch_start, batch_end + 1):
            create_ssh_tunnel(port, remote_host, 3389, ssh_key_path, ssh_user, ssh_host, ssh_port, error_ports)
        print(f"Batch {batch_start}-{batch_end} completed")
        time.sleep(5)  # 각 배치 완료 후 5초 대기

    if error_ports:
        print(f"Errors occurred on ports: {', '.join(map(str, error_ports))}")
    else:
        print(f"All tunnels created successfully for ports {start_port} to {end_port}")

if __name__ == "__main__":
    ssh_key_path = os.path.expanduser("~/.ssh/id_rsa")
    ssh_user = "root"
    ssh_host = "1.1.1.1" # 터널링을 하기 위한 목적지 IP
    ssh_port = 40002

    remote_host = "localhost"
    start_port = 20000
    end_port = 20399  # 400개의 포트만 설정

    batch_size = 100  # 한 번에 처리할 포트 수

    # 기존의 SSH 터널링을 모두 종료합니다
    terminate_existing_tunnels()

    start_time = time.time()

    create_tunnels_in_batches(start_port, end_port, batch_size, remote_host, ssh_key_path, ssh_user, ssh_host, ssh_port)

    end_time = time.time()
    print(f"SSH tunnels created for ports {start_port}-{end_port}")
    print(f"Execution time: {end_time - start_time:.2f} seconds")
