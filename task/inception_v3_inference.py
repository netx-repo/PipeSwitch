import contextlib
import threading
import time

import torch
import numpy

import task.inception_v3 as inception_v3
import task.common as util

TASK_NAME = 'inception_v3_inference'

@contextlib.contextmanager
def timer(prefix):
    _start = time.time()
    yield
    _end = time.time()
    print(prefix, 'cost', _end - _start)

def import_data_loader():
    return None

def import_model():
    model = inception_v3.import_model()
    model.eval()
    return model

def import_func():
    def inference(model, data_b):
        print(threading.currentThread().getName(),
            'inception_v3 inference >>>>>>>>>>', time.time(),
            'model status', model.training)
        with timer('inception_v3 inference func'):
            data = torch.from_numpy(numpy.frombuffer(data_b, dtype=numpy.float32))
            input_batch = data.view(-1, 3, 299, 299).cuda(non_blocking=True)
            with torch.no_grad():
                output = model(input_batch)
            return output.sum().item()
    return inference

def import_task():
    model = import_model()
    func = import_func()
    group_list = inception_v3.partition_model(model)
    group_list = [group for group in group_list if 'AuxLogits' not in group[0].fullname]
    shape_list = [util.group_to_shape(group) for group in group_list]
    return model, func, shape_list


def import_parameters():
    model = import_model()
    group_list = inception_v3.partition_model(model)
    group_list = [group for group in group_list if 'AuxLogits' not in group[0].fullname]
    batch_list = [util.group_to_batch(group) for group in group_list]
    return batch_list
