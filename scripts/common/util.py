import os

class RunRemoteRepo:
    def __init__(self, server, branch):
        self.server = server
        self.branch = branch

    def __enter__(self):
        os.system("ssh %s 'git clone --branch %s https://github.com/baizh1994/PipeSwitch.git'" % (self.server['id'], self.branch))
        return self

    def __exit__(self, *args, **kwargs):
        os.system("ssh %s 'rm -rf ~/PipeSwitch'" % self.server['id'])

    def run(self, cmd):
        os.system("ssh %s '%s'" % (self.server['id'], cmd))

class RunDocker:
    def __init__(self, image, label, branch):
        self.image = image
        self.name = 'pipeswitch-%s' % label
        self.branch = branch

    def __enter__(self):
        os.system('docker run --name %s --rm -it -d --gpus all -w /workspace %s bash' % (self.name, self.image))
        self.run('docker exec -it -w /workspace %s git clone --branch %s https://github.com/baizh1994/PipeSwitch.git' % (self.name, self.branch))
        return self

    def __exit(self, *args, **kwargs):
        os.system('docker stop %s' % self.name)

    def run(self, cmd):
        os.system('docker exec -it -w /workspace %s %s' % (self.name, cmd))

def import_server_list(path):
    server_list = []
    with open(path) as f:
        for line in f.readlines():
            parts = line.split(',')
            ser_ip_str = parts[0].strip()
            ser_name = parts[1].strip()
            server_list.append({'ip': ser_ip_str, 'id': ser_name})
    return server_list