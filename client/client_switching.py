import sys
import time
import struct
import statistics

from experiments.helper import get_data
from core.util import TcpClient, timestamp

def send_request(client, task_name, data):
    timestamp('client', 'before_request_%s' % task_name)

    # Serialize data
    task_name_b = task_name.encode()
    task_name_length = len(task_name_b)
    task_name_length_b = struct.pack('I', task_name_length)

    if data is not None:
        data_b = data.numpy().tobytes()
        length = len(data_b)
    else:
        data_b = None
        length = 0
    length_b = struct.pack('I', length)
    timestamp('client', 'after_inference_serialization')

    # Send Data
    client.send(task_name_length_b)
    client.send(task_name_b)
    client.send(length_b)
    if data_b is not None:
        client.send(data_b)
    timestamp('client', 'after_request_%s' % task_name)

def recv_response(client):
    reply_b = client.recv(4)
    reply = reply_b.decode()
    timestamp('client', 'after_reply')

def close_connection(client):
    model_name_length = 0
    model_name_length_b = struct.pack('I', model_name_length)
    client.send(model_name_length_b)
    timestamp('client', 'close_connection')

def main():
    model_name = sys.argv[1]
    batch_size = int(sys.argv[2])

    task_name_inf = '%s_inference' % model_name
    task_name_train = '%s_training' % model_name

    # Load image
    data = get_data(model_name, batch_size)

    latency_list = []
    for _ in range(20):
        # Send training request
        client_train = TcpClient('localhost', 12345)
        send_request(client_train, task_name_train, None)
        time.sleep(4)

        # Connect
        client_inf = TcpClient('localhost', 12345)
        timestamp('client', 'after_inference_connect')
        time_1 = time.time()

        # Send inference request
        send_request(client_inf, task_name_inf, data)

        # Recv inference reply
        recv_response(client_inf)
        time_2 = time.time()
        latency = (time_2 - time_1) * 1000
        latency_list.append(latency)

        time.sleep(1)
        recv_response(client_train)
        close_connection(client_inf)
        close_connection(client_train)
        time.sleep(1)
        timestamp('**********', '**********')

    print()
    print()
    print()
    stable_latency_list = latency_list[10:]
    print (stable_latency_list)
    print ('Latency: %f ms (stdev: %f)' % (statistics.mean(stable_latency_list), 
                                           statistics.stdev(stable_latency_list)))

if __name__ == '__main__':
    main()
