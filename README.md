# High-level Python SKIL client

## Installation

```bash
python setup.py install
```

## Example usage

```python
from skil import Skil, WorkSpace, Experiment, Model, Deployment

# Define and persist your model first
model_path = './tf_graph.pb'

# connect to your running skil instance
skil_server = Skil(model_server_id='dec0bbde-bf81-45cf-b223-f88c24d0ff99')
skil_server.upload_model(model_path)

# create a workspace and an experiment in it
ws = WorkSpace(skil_server, 'jupyter_ws')
experiment = Experiment(ws, 'test_exp')

# add your model to SKIL
model = Model(experiment, model_path, id='model_id',
                name='model', version=1)
model.add_evaluation(id='eval', name='eval', version=1, accuracy=0.93)

# deploy the model
deployment = Deployment(skil_server, 'test_deployment')
model.deploy(deployment)
```
