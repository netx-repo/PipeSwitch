import os
import sys
import time
import struct
import statistics

import torch

from util import TcpClient, timestamp
import task.inception_v3 as inception_v3

def main():
    # Load image
    data, _ = inception_v3.import_data(1)

    latency_list = []
    for _ in range(20):
        timestamp('client', 'before_request')

        # Connect
        client = TcpClient('localhost', 12345)
        timestamp('client', 'after_connect')
        time_1 = time.time()

        # Serialize data
        model_name = 'inception_v3_inference'
        model_name_b = model_name.encode()
        model_name_length = len(model_name_b)
        model_name_length_b = struct.pack('I', model_name_length)
        data_b = data.numpy().tobytes()
        length = len(data_b)
        length_b = struct.pack('I', length)
        timestamp('client', 'after_serialization')

        # Send Data
        client.send(model_name_length_b)
        client.send(model_name_b)
        client.send(length_b)
        client.send(data_b)
        timestamp('client', 'after_send')

        # Get reply
        reply_b = client.recv(4)
        reply = reply_b.decode()
        if reply == 'FAIL':
            break
        timestamp('client', 'after_reply')
        time_2 = time.time()

        model_name_length = 0
        model_name_length_b = struct.pack('I', model_name_length)
        client.send(model_name_length_b)
        timestamp('client', 'close_training_connection')

        timestamp('**********', '**********')
        latency = (time_2 - time_1) * 1000
        latency_list.append(latency)
        
        time.sleep(1)

    print()
    print()
    print()
    stable_latency_list = latency_list[10:]
    print ('Latency: %f ms (stdev: %f)' % (statistics.mean(stable_latency_list), 
                                           statistics.stdev(stable_latency_list)))

if __name__ == '__main__':
    main()
