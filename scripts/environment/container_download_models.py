from task.helper import get_data, get_model

def main():
    for model_name in ['resnet152', 'inception_v3', 'bert_base']:
        get_model(model_name)

if __name__ == '__main__':
    main()