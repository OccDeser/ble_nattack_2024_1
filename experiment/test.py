import os
from argparse import ArgumentParser

from utils.server import Server
from utils.docker import load_image, is_container_exist, IMAGE_NAME, IMAGE_VERSION

MODEL_DIR = './model'

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--ssh-ip', type=str)
    parser.add_argument('--ssh-port', type=int)
    parser.add_argument('--ssh-username', type=str)
    parser.add_argument('--ssh-password', type=str)
    parser.add_argument('--ssh-workdir', type=str, default='/home/itachi/ble/temp')
    parser.add_argument('--container-port', type=int, default=61322)
    parser.add_argument('--container-name', type=str, default='tamarin-ble-entropy')
    parser.add_argument('--stop', action='store_true')
    args = parser.parse_args()

    ssh_ip = args.ssh_ip
    ssh_port = args.ssh_port
    ssh_username = args.ssh_username
    ssh_password = args.ssh_password
    ssh_workdir = args.ssh_workdir
    container_port = args.container_port
    container_name = args.container_name
    
    stop = args.stop
    server = Server(ssh_ip, ssh_port, ssh_username, ssh_password, ssh_workdir)
    server.connect()
    
    if stop:
        if is_container_exist(server, container_name):
            server.excute(f'docker rm -f {container_name}')
        exit(0)

    load_image(server)

    # send model files to server
    server.excute(f'[ -d {MODEL_DIR} ] && rm -r {MODEL_DIR}')
    server.excute(f'mkdir -p {MODEL_DIR}')
    for file in os.listdir(MODEL_DIR):
        if file.endswith('.spthy'):
            spthy = f"{MODEL_DIR}/{file}"
            server.copy_file_to_workdir(spthy, spthy)

    # start container
    if is_container_exist(server, container_name):
        server.excute(f'docker rm -f {container_name}')
        
    server.excute(f"""docker run --rm -d \
        -p {container_port}:3001 \
        -v {ssh_workdir}/{MODEL_DIR}:/work \
        --name={container_name} {IMAGE_NAME}:{IMAGE_VERSION} \
        tamarin-prover interactive --derivcheck-timeout=0 --image-format=PNG --interface=0.0.0.0 /work
    """)
