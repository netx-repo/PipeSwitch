import os
import sys

from scripts.common.util import RunDocker

def main():
    with RunDocker('mps:mps', 'figure6_mps_10s') as rd:
        # Start the server: mps
        rd.run('python mps/scripts/run_data.py')
        
        # Get and return the data point

if __name__ == '__main__':
    main()