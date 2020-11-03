# Client

This folder contains codes for clients.

# Files

- client_inference.py: In each iteration, send an inferece request, wait for the reply and record the latency without switching.
- client_switching.py: In each iteration, send a training request, then send an inference request to record the latency with switching.

# Environment
You need to add the path to the repo to `PYTHONPATH`.

# Usage

## client_inference

```
python client_inference.py [model_name] [batch_size]
```
`model_name` can be `resnet152`, `inception_v3` or `bert_base`.

Example:

```
python client_inference.py resnet152 8
```

## client_switching

```
python client_switching.py [model_name] [batch_size]
```
`model_name` can be `resnet152`, `inception_v3` or `bert_base`.

Example:

```
python client_switching.py resnet152 8
```