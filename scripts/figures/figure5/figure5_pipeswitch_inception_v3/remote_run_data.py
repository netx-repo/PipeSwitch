import os

from scripts.common.util import RunDocker

def main():
    with RunDocker('pipeswitch:pipeswitch', 'pipeswitch', 'figure5_pipeswitch_inception_v3') as rd:
        # Start the server: pipeswitch
        rd.run('python PipeSwitch/scripts/run_data.py')
        
        # Get and return the data point

if __name__ == '__main__':
    main()