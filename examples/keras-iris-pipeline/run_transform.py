import skil
import numpy as np

skil_server = skil.Skil()
work_space = skil.WorkSpace(skil_server)
experiment = skil.Experiment(work_space)

transform = skil.Transform(transform='iris_tp.json', experiment=experiment)
deployment = skil.Deployment(skil_server)
service = transform.deploy(deployment)

with open('iris.data', 'r') as f:
    data = np.array(f.readlines())

print(service.predict(data))
