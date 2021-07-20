from os import name
from task.resnet152_training import import_data_loader, import_model, import_func
from task.helper import get_data, get_model

def warm_up_training():
    # Warm up training
    data_loader = import_data_loader()
    model = import_model().cuda()
    func = import_func()
    func(model, data_loader)

def warm_up_inference(model_name):
    # Warm up training
    data = get_data(model_name, 8)
    model, func = get_model(model_name)

    model = model.cuda()
    data_b = data.numpy().tobytes()
    func(model, data_b)

def main():
    warm_up_training()

    # Warmup inference
    for model_name in ['resnet152', 'inception_v3', 'bert_base']:
        warm_up_inference(model_name)
    


if __name__ == '__main__':
    main()