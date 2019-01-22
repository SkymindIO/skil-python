import skil
import pyspark
import numpy as np

skil_server = skil.Skil()
work_space = skil.WorkSpace(skil_server)
experiment = skil.Experiment(work_space)

transform = skil.Transform(transform='iris_tp.json', experiment=experiment)
model = skil.Model(model='iris_model.h5', experiment=experiment)
deployment = skil.Deployment(skil_server)

pipeline = skil.Pipeline(deployment, model, transform)

with open('iris.data', 'r') as f:
    data = np.array(f.readlines())

print(pipeline.predict(data))