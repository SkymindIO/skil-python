# Deploying a Keras model with SKIL in 60 seconds

## Start SKIL with docker

```bash
sudo docker pull skymindops/skil-ce
sudo docker run --rm -it -p 9008:9008 -p 8080:8080 skymindops/skil-ce bash /start-skil.sh
```

## Install Python SKIL client, train and persist a Keras model

```bash
git clone https://github.com/SkymindIO/skil-python
cd examples/keras-mnist-mlp
virtualenv venv && source venv/bin/activate
pip install skil
pip install tensorflow keras
python train.py
```

## Deploy model with SKIL

```python
from skil import Skil, WorkSpace, Experiment, Model, Deployment
skil_server = Skil()

work_space = WorkSpace(skil_server, 'test-workspace')
experiment = Experiment(work_space, 'test-experiment')

model_name = 'keras-mnist-mlp.h5'
model = Model(experiment, model_name, id='1337', name='keras-mnist', version=1)
model.add_evaluation(id='42', name='eval-keras-mnist', version=1, accuracy=0.995)

deployment = Deployment(skil_server, 'keras-deployment')
model.deploy(deployment)

model.serve()
```
                                                                                                                    1 ↵
