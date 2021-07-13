import time
import threading
import importlib
import multiprocessing as mp

class PauseThd(threading.Thread):
    def __init__(self, pipe, PAUSE_SIGNAL):
        super(PauseThd, self).__init__()
        self.pipe = pipe
        self.PAUSE_SIGNAL = PAUSE_SIGNAL

    def run(self):
        while True:
            msg = self.pipe.recv()
            if msg == 'PAUSE':
                self.PAUSE_SIGNAL[0] = 1
            else:
                self.PAUSE_SIGNAL[0] = 0


class TrainProc(mp.Process):
    def __init__(self, model_name, pipe):
        super(TrainProc, self).__init__()
        self.model_name = model_name
        self.pipe = pipe
        self.PAUSE_SIGNAL = [0]
        
    def run(self):
        model_module = importlib.import_module('task.' + self.model_name + '_training')
        model = model_module.import_model()
        func = model_module.import_func()
        data_loader = model_module.import_data_loader()

        def hook_for_pause(mod, input, output):
            while self.PAUSE_SIGNAL[0] == 1:
                time.sleep(0.01)
        def travel_layers(mod):
            if len(list(mod.children())) == 0:
                mod.register_forward_hook(hook_for_pause)
                mod.register_backward_hook(hook_for_pause)
            else:
                for child in mod.children():
                    travel_layers(child)
        travel_layers(model)

        t_pause = PauseThd(self.pipe, self.PAUSE_SIGNAL)
        t_pause.start()

        model = model.cuda()
        while True:
            func(model, data_loader)