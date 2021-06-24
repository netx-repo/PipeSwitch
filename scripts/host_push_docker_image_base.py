import os
import sys

from util import import_server_list

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

        print ('%s> Clone PipeSwitch repo' % server['id'])
        os.system("ssh %s'git clone --branch dev https://github.com/baizh1994/PipeSwitch.git'" % server['id'])
        print ('%s> Complete cloning PipeSwitch repo' % server['id'])

        print ('%s> Load docker image for base' % server['id'])
        os.system("ssh %s 'bash ~/PipeSwitch/scripts/server_load_docker_image_base.sh'" % server['id'])
        print ('%s> Complete loading docker image for base' % server['id'])

if __name__ == '__main__':
    main()