import threading
import struct

from util.util import timestamp


class FrontendTcpThd(threading.Thread):
    def __init__(self, qout, agent):
        super(FrontendTcpThd, self).__init__()
        self.qout = qout
        self.agent = agent

    def run(self):
        while True:
            timestamp('tcp', 'listening')
            
            model_name_length_b = self.agent.recv(4)
            model_name_length = struct.unpack('I', model_name_length_b)[0]
            if model_name_length == 0:
                break
            model_name_b = self.agent.recv(model_name_length)
            model_name = model_name_b.decode()
            self.qout.put((self.agent, model_name))
            timestamp('tcp', 'get_name')

            data_length_b = self.agent.recv(4)
            data_length = struct.unpack('I', data_length_b)[0]
            if data_length > 0:
                data_b = self.agent.recv(data_length)
            else:
                data_b = None
            timestamp('tcp', 'get_data')
            self.qout.put(data_b)
            timestamp('tcp', 'enqueue_request')
