import time

import torch
import torch.nn as nn

import task.inception_v3 as inception_v3
import task.common as util

TASK_NAME = 'inception_v3_training'

def import_data_loader():
    return inception_v3.import_data

def import_model():
    model = inception_v3.import_model()
    model.train()
    return model

def import_func():
    def train(model, data_loader):
        # Prepare data
        #batch_size = 32
        batch_size = 8
        images, target = data_loader(batch_size)

        # Prepare training
        lr = 0.1
        momentum = 0.9
        weight_decay = 1e-4
        criterion = nn.CrossEntropyLoss().cuda()
        optimizer = torch.optim.SGD(model.parameters(), lr, momentum=momentum, weight_decay=weight_decay)

        loss = None
        for i in range(100):
            # Data to GPU
            images = images.cuda(non_blocking=True)
            target = target.cuda(non_blocking=True)

            # compute output
            output = model(images)
            loss = criterion(output[0], target)

            # compute gradient and do SGD step
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            print ('Training', i, time.time(), loss.item())
        return loss.item()
    return train

def import_task():
    model = import_model()
    func = import_func()
    group_list = inception_v3.partition_model(model)
    shape_list = [util.group_to_shape(group) for group in group_list]
    return model, func, shape_list


def import_parameters():
    model = import_model()
    group_list = inception_v3.partition_model(model)
    batch_list = [util.group_to_batch(group) for group in group_list]
    return batch_list
