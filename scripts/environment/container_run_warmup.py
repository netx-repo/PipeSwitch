from task.resnet152_training import import_data_loader, import_model, import_func

def main():
    data_loader = import_data_loader()
    model = import_model().cuda()
    func = import_func()
    func(model, data_loader)

if __name__ == '__main__':
    main()