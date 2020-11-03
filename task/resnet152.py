import os

import torch

import task.common as util

MODEL_NAME = 'resnet152'

def import_data(batch_size):
    filename = 'dog.jpg'

    # Download an example image from the pytorch website
    if not os.path.isfile(filename):
        import urllib
        url = 'https://github.com/pytorch/hub/raw/master/dog.jpg'
        try: 
            urllib.URLopener().retrieve(url, filename)
        except: 
            urllib.request.urlretrieve(url, filename)

    # sample execution (requires torchvision)
    from PIL import Image
    from torchvision import transforms
    input_image = Image.open(filename)
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    input_tensor = preprocess(input_image)
    image = input_tensor.unsqueeze(0) # create a mini-batch as expected by the model

    images = torch.cat([image] * batch_size)
    target = torch.tensor([0] * batch_size)
    return images, target

def import_model():
    model = torch.hub.load('pytorch/vision:v0.4.2',
                           MODEL_NAME,
                           pretrained=True)
    util.set_fullname(model, MODEL_NAME)

    return model

def partition_model(model):
    group_list = []
    before_core = []
    core_complete = False
    after_core = []

    group_list.append(before_core)
    for name, child in model.named_children():
        if 'layer' in name:
            core_complete = True
            for _, child_child in child.named_children():
                group_list.append([child_child])
        else:
            if not core_complete:
                before_core.append(child)
            else:
                after_core.append(child)
    group_list.append(after_core)

    return group_list