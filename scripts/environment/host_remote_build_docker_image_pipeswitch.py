import os
import sys

from util import import_server_list

def main():
    server_list_path = sys.argv[1]
    print (server_list_path)

    server_list = import_server_list(server_list_path)

    for server in server_list:
        print ('%s> Build docker image for pipeswitch' % server['id'])
        os.system("ssh %s 'bash ~/PipeSwitch/scripts/server_build_docker_image_pipeswitch.sh'" % server['id'])
        print ('%s> Complete building docker image for pipeswitch' % server['id'])

if __name__ == '__main__':
    main()