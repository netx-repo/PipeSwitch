import os
import sys

from scripts.common.util import RunRemoteRepo, import_server_list

def main():
    server_list_path = sys.argv[1]
    label = sys.argv[2]

    server_list = import_server_list(server_list_path)

    with RunRemoteRepo(server_list[0], 'dev') as rrr:
        rrr.run("bash ~/PipeSwitch/scripts/figures/figure5/remote_run_data.sh %s" % label)

if __name__ == '__main__':
    main()