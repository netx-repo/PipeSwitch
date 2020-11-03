import os
import sys
import time
import struct
import statistics

import torch

from util import TcpClient, timestamp
import task.bert_base as bert_base

def send_inference_request(client, data):
    timestamp('client', 'before_inference_request')

    # Serialize data
    model_name = 'bert_base_inference'
    model_name_b = model_name.encode()
    model_name_length = len(model_name_b)
    model_name_length_b = struct.pack('I', model_name_length)
    data_b = data.numpy().tobytes()
    length = len(data_b)
    length_b = struct.pack('I', length)
    timestamp('client', 'after_inference_serialization')

    # Send Data
    client.send(model_name_length_b)
    client.send(model_name_b)
    client.send(length_b)
    client.send(data_b)
    timestamp('client', 'after_inference_send')

    return client

def recv_inference_response(client):
    reply_b = client.recv(4)
    reply = reply_b.decode()
    timestamp('client', 'after_inference_reply')

def close_inference_connection(client):
    model_name_length = 0
    model_name_length_b = struct.pack('I', model_name_length)
    client.send(model_name_length_b)
    timestamp('client', 'close_inference_connection')

def send_training_request():
    time_1 = time.time()
    timestamp('client', 'before_training_request')

    # Connect
    client = TcpClient('localhost', 12345)
    timestamp('client', 'after_training_connect')

    # Serialize data
    model_name = 'bert_base_training'
    model_name_b = model_name.encode()
    model_name_length = len(model_name_b)
    model_name_length_b = struct.pack('I', model_name_length)
    length = 0
    length_b = struct.pack('I', length)
    timestamp('client', 'after_training_serialization')

    # Send Data
    client.send(model_name_length_b)
    client.send(model_name_b)
    client.send(length_b)
    timestamp('client', 'after_training_send')

    return client

def recv_training_response(client):
    reply_b = client.recv(4)
    reply = reply_b.decode()
    timestamp('client', 'after_training_reply')

def close_training_connection(client):
    model_name_length = 0
    model_name_length_b = struct.pack('I', model_name_length)
    client.send(model_name_length_b)
    timestamp('client', 'close_training_connection')

def main():
    # Load image
    data, _ = bert_base.import_data(1)

    latency_list = []
    for _ in range(20):
        # Send training request
        client_training = send_training_request()
        time.sleep(4)

        # Connect
        client = TcpClient('localhost', 12345)
        timestamp('client', 'after_inference_connect')
        time_1 = time.time()

        # Send inference request
        client_inference = send_inference_request(client, data)

        # Recv inference reply
        recv_inference_response(client_inference)
        time_2 = time.time()
        latency = (time_2 - time_1) * 1000
        latency_list.append(latency)

        time.sleep(1)
        recv_training_response(client_training)
        close_inference_connection(client_inference)
        close_training_connection(client_training)
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
