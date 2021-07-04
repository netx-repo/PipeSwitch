import os
import sys

from scripts.common.util import RunRemoteRepo, import_server_list

def main():
    server_list_path = sys.argv[1]
    print (server_list_path)

    server_list = import_server_list(server_list_path)

    for server in server_list:
        print ('%s> Build docker image for ready_model' % server['id'])
        with RunRemoteRepo(server, 'dev') as rrr:
            rrr.run("bash ~/PipeSwitch/scripts/environment/server_build_docker_image_ready_model.sh")
        print ('%s> Complete building docker image for ready_model' % server['id'])

if __name__ == '__main__':
    main()