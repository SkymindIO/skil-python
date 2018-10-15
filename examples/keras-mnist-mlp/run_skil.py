from skil import Skil, WorkSpace, Experiment, Model, Deployment
import json

# Initialize a new experiment in a workspace
skil_server = Skil()
ws = WorkSpace(skil_server)
experiment = Experiment(ws)
deployment = Deployment(skil_server, "keras_models")

skil_models = []
for epoch in range(2):
    model_name = 'model_{epoch:02d}.hdf5'.format(epoch=epoch + 1)
    model = Model(model_name, id=epoch, experiment=experiment)
    model.deploy(start_server=False, deployment=deployment)
    skil_models.append(model)

with open('history.json', 'r') as f:
    history = json.loads(f.read())
    acc = history.get('val_acc')
best_model = skil_models[acc.index(max(acc))]
best_model.serve()