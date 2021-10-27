import os
import sys

from scripts.common.util import RunRemoteRepo, import_server_list

def main():
    server_list_path = sys.argv[1]
    print (server_list_path)

    server_list = import_server_list(server_list_path)

    for server in server_list:
        print ('%s> Warm up the server' % server['id'])
        with RunRemoteRepo(server, 'dev') as rrr:
            rrr.run("bash ~/PipeSwitch/scripts/environment/server_run_warmup.sh")
        print ('%s> Complete warming up the server' % server['id'])

if __name__ == '__main__':
    main()