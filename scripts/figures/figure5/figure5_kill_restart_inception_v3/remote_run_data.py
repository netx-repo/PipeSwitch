import os

from scripts.common.util import RunDocker

def main():
    with RunDocker('pipeswitch:ready_model', 'pipeswitch', 'figure5_kill_restart_inception_v3') as rd:
        # Start the server: ready_model
        rd.run('python PipeSwitch/scripts/run_data.py')
        
        # Get and return the data point

if __name__ == '__main__':
    main()