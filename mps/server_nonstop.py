import sys
import queue
import struct
import threading
import importlib

import torch
import torch.multiprocessing as mp

from experiments.util import TcpServer, TcpAgent, timestamp
from experiments.server_nonstop.train import TrainProc
from experiments.server_nonstop.inference import InferProc

def func_get_request(active_model_name, qout):
    # Listen connections
    server = TcpServer('localhost', 12345)

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

        if 'training' in model_name:
            agent.send(b'FNSH')
            del agent
        else:
            qout.put((agent, data_b))

def func_schedule(qin, p_train, p_child):
    while True:
        agent, data_b = qin.get()
        p_child.send((agent, data_b))
        #p_train.send('PAUSE')
        p_child.recv()
        #p_train.send('START')

def main():
    # Get model name
    model_name = sys.argv[1]

    # Create worker process
    train_parent, train_child = mp.Pipe()
    p_train = TrainProc(model_name, train_child)
    p_train.start()
    infer_parent, infer_child = mp.Pipe()
    p_infer = InferProc(model_name, infer_child)
    p_infer.start()

    # Create threads and worker process
    q_to_schedule = queue.Queue()
    t_get = threading.Thread(target=func_get_request, args=(model_name, q_to_schedule))
    t_get.start()
    t_schedule = threading.Thread(target=func_schedule, args=(q_to_schedule, train_parent, infer_parent))
    t_schedule.start()

    # Accept connection
    t_get.join()
    t_schedule.join()
    p_train.join()
    p_infer.join()
    

if __name__ == '__main__':
    mp.set_start_method('spawn')
    main()