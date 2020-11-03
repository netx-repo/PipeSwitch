import time

import torch
import torch.nn as nn

import task.bert_base as bert_base
import task.common as util

TASK_NAME = 'bert_base_training'

def import_data_loader():
    return bert_base.import_data

def import_model():
    model = bert_base.import_model()
    model.train()
    return model

def import_func():
    def train(model, data_loader):
        # Prepare data
        batch_size = 32
        data, target = data_loader(batch_size)

        # Prepare training
        criterion = nn.MSELoss().cuda()
        optimizer = torch.optim.SGD(model.parameters(), lr=0.1)

        loss = None
        for i in range(1000):
            # Data to GPU
            data_cuda = data.view(2, -1, 251).cuda()
            target_0_cuda = target[0].cuda()
            target_1_cuda = target[1].cuda()

            # compute output
            output = model(data_cuda[0], token_type_ids=data_cuda[1])
            loss1 = criterion(output[0], target_0_cuda)
            loss2 = criterion(output[1], target_1_cuda)
            loss = loss1 + loss2

            # compute gradient and do SGD step
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            print ('Training', i, time.time(), loss.item())
            del data_cuda
            del target_0_cuda
            del target_1_cuda

        return loss
    
    return train

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