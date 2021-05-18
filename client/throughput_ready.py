import sys
import time
import struct
import statistics

from task.helper import get_data
from util.util import TcpClient, timestamp

def main():
    model_name = sys.argv[1]
    batch_size = int(sys.argv[2])
    scheduling_cycle = int(sys.argv[3])

    # Load image
    data = get_data(model_name, batch_size)

    throughput_list = []
    for _ in range(20):
        timestamp('client', 'before_request')

        # Connect
        client = TcpClient('localhost', 12345)
        timestamp('client', 'after_connect')


        #count
        inference_count = 0
        time_count = scheduling_cycle
        while (time_count > 0):
            time_1 = time.time()

            # Serialize data
            task_name = model_name + '_inference'
            task_name_b = task_name.encode()
            task_name_length = len(task_name_b)
            task_name_length_b = struct.pack('I', task_name_length)
            data_b = data.numpy().tobytes()
            length = len(data_b)
            length_b = struct.pack('I', length)
            timestamp('client', 'after_serialization')

            # Send Data
            client.send(task_name_length_b)
            client.send(task_name_b)
            client.send(length_b)
            client.send(data_b)
            timestamp('client', 'after_send')

            # Get reply
            reply_b = client.recv(4)
            reply = reply_b.decode()
            if reply == 'FAIL':
                timestamp('client', 'FAIL')
                break
            timestamp('client', 'after_reply')
            time_2 = time.time()

            time_count -= (time_2 - time_1)
            #If time exceeds, do not count this iteration
            if (time_count > 0):
                inference_count += 1
        throughput_list.append(inference_count)

        model_name_length = 0
        model_name_length_b = struct.pack('I', model_name_length)
        client.send(model_name_length_b)
        timestamp('client', 'close_training_connection')

        timestamp('**********', '**********')
        
        # time.sleep(1)

    print()
    print()
    print()
    stable_throughput_list = throughput_list[10:]
    value = (statistics.mean(stable_throughput_list)) / scheduling_cycle
    print ('Latency: %f ms (stdev: %f)' % (value, 
                                           statistics.stdev(stable_latency_list)))

if __name__ == '__main__':
    main()