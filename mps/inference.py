import importlib

import torch.multiprocessing as mp

class InferProc(mp.Process):
    def __init__(self, model_name, pipe):
        super(InferProc, self).__init__()
        self.model_name = model_name
        self.pipe = pipe
        
    def run(self):
        # Load model
        model_module = importlib.import_module('task.' + self.model_name + '_inference')
        model = model_module.import_model()
        func = model_module.import_func()

        # Model to GPU
        model = model.eval().cuda()

        while True:
            agent, data_b = self.pipe.recv()
            output = func(model, data_b)
            print (output)
            agent.send(b'FNSH')
            self.pipe.send('FNSH')
            del agent