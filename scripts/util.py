def import_server_list(path):
    server_list = []
    with open(path) as f:
        for line in f.readlines():
            parts = line.split(',')
            ser_ip_str = parts[0].strip()
            ser_name = parts[1].strip()
            server_list.append({'ip': ser_ip_str, 'id': ser_name})
    return server_list