import paramiko
import threading


class Server(object):
    def __init__(self, host, port, username, password, workdir, workers=1, weight=1) -> None:
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.workdir = workdir
        self.workers = workers
        self.weight = weight
        self.finished = True
        self.ssh = None
        self.sftp = None
        self.cases = []
        self.lock = threading.Lock()

    def connect(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.host, self.port, self.username, self.password)
        self.ssh = ssh
        self.sftp = ssh.open_sftp()
        self.ssh.exec_command(f'mkdir -p {self.workdir}')

    def close(self):
        self.ssh.close()
        self.sftp.close()

    def excute(self, command):
        # excute command
        command = f'cd {self.workdir}; {command}'
        self.lock.acquire()
        stdin, stdout, stderr = self.ssh.exec_command(command)
        self.lock.release()
        stdout = stdout.read().decode('utf-8')
        stderr = stderr.read().decode('utf-8')
        if stderr:
            print(f'Error on {self.host}: {stderr}')
        return stdout, stderr

    def copy_file_to_workdir(self, local, remote):
        remote = f"{self.workdir}/{remote}"
        self.lock.acquire()
        self.sftp.put(local, remote)
        self.lock.release()

    def copy_file_from_workdir(self, remote, local):
        remote = f"{self.workdir}/{remote}"
        self.lock.acquire()
        self.sftp.get(remote, local)
        self.lock.release()
