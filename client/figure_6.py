import subprocess
import time

#model_names = ['resnet152', 'inception_v3', 'bert_base']
batch_size = 8
scheduling_cycle = ['1','2','5','10','30']

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

def request(model, scheduling_cycle, batch_size=8):
    p = subprocess.Popen(['python','throughput.py',model,str(batch_size), scheduling_cycle])
    p.wait()

def request_ready(model, scheduling_cycle, batch_size=8):
    p = subprocess.Popen(['python','throughput_ready.py',model,str(batch_size),scheduling_cycle])
    p.wait()


m = 'resnet152'
#ready_model
for t in scheduling_cycle:
    p = ready_server(m)
    request_ready(m, scheduling_cycle=t)
    p.kill()
    print("-------------------")
    time.sleep(5)

#pipeswitch
for t in scheduling_cycle:
    p = pipe_server()
    request(m, scheduling_cycle=t)
    p.kill()
    print("-------------------")
    time.sleep(5)

#kill_restart
for t in scheduling_cycle:
    p = kill_start_server()
    request(m, scheduling_cycle=t)
    p.kill()
    print("-------------------")
    time.sleep(5)

print("figure 6 is done.")