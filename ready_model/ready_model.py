import sys
import queue
import struct
import threading
import importlib

import torch
import torch.multiprocessing as mp

from task.helper import get_model
from util.util import TcpServer, TcpAgent, timestamp

def func_get_request(active_model_name, qout):
    # Listen connections
    server = TcpServer('localhost', 12345)
    print("Start listening...")

    while True:
        # Get connection
        conn, _ = server.accept()
        agent = TcpAgent(conn)

        model_name_length_b = agent.recv(4)
        model_name_length = struct.unpack('I', model_name_length_b)[0]
        if model_name_length == 0:
            break
        model_name_b = agent.recv(model_name_length)
        model_name = model_name_b.decode()
        if active_model_name not in model_name:
            raise Exception('Invalid model name')
        timestamp('tcp', 'get_name')

        data_length_b = agent.recv(4)
        data_length = struct.unpack('I', data_length_b)[0]
        if data_length > 0:
            data_b = agent.recv(data_length)
        else:
            data_b = None
        timestamp('tcp', 'get_data')
        qout.put((agent, data_b))

def func_schedule(qin, pipe):
    print("Start scheduling...")
    while True:
        agent, data_b = qin.get()
        pipe.send((agent, data_b))

<<<<<<< HEAD
def worker_compute(model_name, pipe): 
=======
def worker_compute(model_name, pipe):
    print("Computing...")
>>>>>>> install all packages
    # Load model
    model, func = get_model(model_name)

    # Model to GPU
    model = model.eval().cuda()

    while True:
        try:
            agent, data_b = pipe.recv()
        except:
            return
            

        # Compute
        output = func(model, data_b)
        timestamp('server', 'complete')

        agent.send(b'FNSH')
        timestamp('server', 'reply')

        del agent

def main():
    # Get model name
    model_name = sys.argv[1]

    # Create threads and worker process
    q_to_schedule = queue.Queue()
    p_parent, p_child = mp.Pipe()
    t_get = threading.Thread(target=func_get_request, args=(model_name, q_to_schedule))
    t_get.start()
    t_schedule = threading.Thread(target=func_schedule, args=(q_to_schedule, p_parent))
    t_schedule.start()
    p_compute = mp.Process(target=worker_compute, args=(model_name, p_child))
    p_compute.start()

    # Accept connection
    t_get.join()
    t_schedule.join()
    p_compute.join()
    

if __name__ == '__main__':
    mp.set_start_method('spawn')
    main()