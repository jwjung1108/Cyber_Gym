import os
import subprocess
from flask import Flask, jsonify, request
import docker
import time
import random
import socket

app = Flask(__name__)
client = docker.from_env()

def find_free_port():
    while True:
        port = random.randint(20000, 20400)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) != 0:
                return port

def get_container_port(container):
    container.reload()
    ports = container.attrs['NetworkSettings']['Ports']
    print(f"Available ports: {ports}")
    for bindings in ports.values():
        if bindings:
            return int(bindings[0]['HostPort'])
    return None

@app.route('/create/<category>/<name>', methods=['POST'])
def create_container(category, name):
    compose_file_path = f"/root/{category}/{name}/docker-compose.yml"
    if not os.path.exists(compose_file_path):
        print(f"Compose file not found at {compose_file_path}")
        return jsonify({"error": "Compose file not found"}), 404

    try:
        # Docker Compose 파일이 있는 디렉토리로 이동
        compose_dir = os.path.dirname(compose_file_path)
        os.chdir(compose_dir)

        # 타임스탬프를 사용하여 고유한 컨테이너 이름 생성
        unique_container_name = f"{category}{name}_{int(time.time())}"
        print(f"Generated unique container name: {unique_container_name}")

        host_port = find_free_port()
        env = os.environ.copy()
        env['CONTAINER_NAME'] = unique_container_name
        env['HOST_PORT'] = str(host_port)

        # Docker Compose를 실행하여 고유한 이름의 새 서비스 인스턴스 시작
        subprocess.run(["docker-compose", "-p", unique_container_name, "up", "-d"], check=True, env=env)

        # 고유한 이름으로 필터링하여 새 컨테이너 찾기
        containers = client.containers.list(filters={"name": unique_container_name})
        if not containers:
            print(f"No containers found with name: {unique_container_name}")
            return jsonify({"error": "Container not found"}), 404

        new_container = containers[0]
        container_name = new_container.name
        port = get_container_port(new_container)

        if port is None:
            print(f"No port found for container: {container_name}")
            return jsonify({"error": "No port found for container"}), 500

        print(f"Container created with name: {container_name} and port: {port}")

        return jsonify({"message": "Container created", "container_name": container_name, "port": port, "title": name}), 201

    except subprocess.CalledProcessError as e:
        print(f"Subprocess error: {e}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print(f"Exception: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/down/<container_name>', methods=['POST'])
def down_container(container_name):
    try:
        # 이름으로 컨테이너 가져오기
        container = client.containers.get(container_name)

        # 컨테이너 중지 및 제거
        container.stop()
        container.remove()
        print(f"Container stopped and removed: {container_name}")
        
        subprocess.run(["docker", "network", "prune", "-f"], check=True)
        print("Unused Docker networks pruned.")
        
        return jsonify({"message": "Container stopped and removed", "container_name": container_name}), 200
        
    except docker.errors.NotFound:
        print(f"Container not found: {container_name}")
        return jsonify({"error": "Container not found"}), 404
    except docker.errors.APIError as e:
        print(f"Docke API error: {e}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print(f"General error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/')
def hello_world():
    print("Hello World endpoint was called")
    return 'Hello World'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
