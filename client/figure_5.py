import subprocess
import time

model_names = ['resnet152', 'inception_v3', 'bert_base']
batch_size = 8

def ready_server(model):
    p = subprocess.Popen(['python','../ready_model/ready_model.py',model]) 
    time.sleep(3)
    return p

def pipe_server():
    p = subprocess.Popen(['python','../pipeswitch/main.py','model_list.txt'])
    return p

def kill_start_server():
    p = subprocess.Popen(['python','../kill_restart/kill_restart.py'])
    return p

def request_ready(model, batch_size=8):
    p = subprocess.Popen(['python','client_inference.py',model,str(batch_size)])
    p.wait()

def request_switch(model, batch_size=8):
    p = subprocess.Popen(['python','client_switching.py',model,str(batch_size)])
    p.wait()

#ready_model
for m in model_names:
    p = ready_server(m)
    request_ready(m)
    p.kill()
    print("-------------------")
    time.sleep(5)

#pipeswitch
for m in model_names:
    p = pipe_server()
    request_switch(m)
    p.kill()
    print("-------------------")
    time.sleep(5)

#kill_restart
for m in model_names:
    p = kill_start_server()
    request_switch(m)
    p.kill()
    print("-------------------")
    time.sleep(5)

print("figure 5 is done.")