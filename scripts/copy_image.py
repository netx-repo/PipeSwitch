import os
import sys

def import_server_list(path):
    server_list = []
    with open(path) as f:
        for line in f.readlines():
            parts = line.split(',')
            ser_ip_str = parts[0].strip()
            ser_name = parts[1].strip()
            server_list.append({'ip': ser_ip_str, 'id': ser_name})
    return server_list

def copy_image(image_path, server_list):
    for server in server_list:
        src = image_path
        dst = server['id'] + ':~/'
        os.system('scp %s %s' % (src, dst))

def main():
    server_list_path = sys.argv[1]
    image_path = sys.argv[2]
    print (server_list_path)
    print (image_path)

    server_list = import_server_list(server_list_path)
    print (server_list)

    copy_image(image_path, server_list)

if __name__ == '__main__':
    main()