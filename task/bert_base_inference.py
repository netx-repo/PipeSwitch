import contextlib
import threading
import time

import torch
import numpy

import task.bert_base as bert_base
import task.common as util

TASK_NAME = 'bert_base_inference'

@contextlib.contextmanager
def timer(prefix):
    _start = time.time()
    yield
    _end = time.time()
    print(prefix, 'cost', _end - _start)

def import_data_loader():
    return None

def import_model():
    model = bert_base.import_model()
    model.eval()
    return model

def import_func():
    def inference(model, data_b):
        print(threading.currentThread().getName(),
            'bert base inference >>>>>>>>>>', time.time(), 'model status',
            model.training)

        with torch.no_grad(), timer('bert_base inf costs'):
            data = torch.from_numpy(numpy.frombuffer(data_b, dtype=numpy.long))
            input_batch = data.view(2, -1, 251).cuda(non_blocking=True)
            output = model(input_batch[0], token_type_ids=input_batch[1])
            return output[0].sum().item()
    return inference

def import_task():
    model = import_model()
    func = import_func()
    group_list = bert_base.partition_model(model)
    shape_list = [util.group_to_shape(group) for group in group_list]
    return model, func, shape_list


def import_parameters():
    model = import_model()
    group_list = bert_base.partition_model(model)
    batch_list = [util.group_to_batch(group) for group in group_list]
    return batch_list
