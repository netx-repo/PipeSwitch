import os

import torch

import task.common as util

MODEL_NAME = "inception_v3"


def import_data(batch_size):
    filename = "dog.jpg"

    # Download an example image from the pytorch website
    if not os.path.isfile(filename):
        import urllib

        url = "https://github.com/pytorch/hub/raw/master/images/dog.jpg"
        try:
            urllib.URLopener().retrieve(url, filename)
        except:
            urllib.request.urlretrieve(url, filename)

    # sample execution (requires torchvision)
    from PIL import Image
    from torchvision import transforms

    input_image = Image.open(filename)
    preprocess = transforms.Compose(
        [
            transforms.Resize(299),
            transforms.CenterCrop(299),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )
    input_tensor = preprocess(input_image)
    image = input_tensor.unsqueeze(0)  # create a mini-batch as expected by the model

    images = torch.cat([image] * batch_size)
    target = torch.tensor([0] * batch_size)
    return images, target


def import_model():
    from torchvision import models

    model = models.inception_v3(pretrained=True)
    util.set_fullname(model, MODEL_NAME)

    return model


def partition_model(model):
    group_list = [[child] for child in model.children()]
    return group_list
