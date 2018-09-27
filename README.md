# High-level Python SKIL client

[![Build Status](https://jenkins.ci.skymind.io/buildStatus/icon?job=skymind/skil-python/master)](https://jenkins.ci.skymind.io/blue/organizations/jenkins/skymind%2Fskil-python/activity)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/SkymindIO/skil-python/blob/master/LICENSE)
[![PyPI version](https://badge.fury.io/py/skil.svg)](https://badge.fury.io/py/skil)

## Installation

```bash
pip install skil
```

## Example usage

Lightning version: SKIL does everything necessary for you under the hood, i.e. creating a production-grade model server with batteries included. 

```python
import skil

skil_server = skil.Skil()

model = skil.Model('your_model.h5')
model.deploy(scale=42)
```

Slightly more extended example:

```python
from skil import Skil, WorkSpace, Experiment, Model, Deployment

# Define and persist your model first
model_path = './tf_graph.pb'

# connect to your running skil instance
skil_server = Skil()

# create a workspace and an experiment in it
work_space = WorkSpace(skil_server)
experiment = Experiment(work_space)

# add your model to SKIL
model = Model(model_path, experiment)

# deploy and serve your model
deployment = Deployment(skil_server)
model.deploy(deployment, start_server=False)
model.serve()
```
