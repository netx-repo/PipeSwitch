import os
import sys

from scripts.common.util import RunRemoteRepo, import_server_list

def main():
    server_list_path = sys.argv[1]
    image_path = sys.argv[2]
    print (server_list_path)
    print (image_path)

    server_list = import_server_list(server_list_path)

    for server in server_list:
        src = image_path
        dst = server['id'] + ':~/'
        
        print ('%s> Copy docker image for base' % server['id'])
        os.system('scp %s %s' % (src, dst))
        print ('%s> Complete copying docker image for base' % server['id'])

        print ('%s> Load docker image for base' % server['id'])
        with RunRemoteRepo(server, 'dev') as rrr:
            rrr.run("bash ~/PipeSwitch/scripts/environment/server_load_docker_image_base.sh")
        print ('%s> Complete loading docker image for base' % server['id'])

        

if __name__ == '__main__':
    main()