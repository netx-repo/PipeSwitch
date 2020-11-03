import threading

class WorkerTermThd(threading.Thread):
    def __init__(self, pipe, complete_queue, TERMINATE_SIGNAL):
        super(WorkerTermThd, self).__init__()
        self.pipe = pipe
        self.complete_queue = complete_queue
        self.TERMINATE_SIGNAL = TERMINATE_SIGNAL
    
    def run(self):
        while True:
            _ = self.pipe.recv()
            if self.TERMINATE_SIGNAL[0] == 0:
                self.pipe.send('IDLE')
            elif self.TERMINATE_SIGNAL[0] == 1:
                self.TERMINATE_SIGNAL[0] = 2
                self.complete_queue.get()
                self.pipe.send('FNSH')