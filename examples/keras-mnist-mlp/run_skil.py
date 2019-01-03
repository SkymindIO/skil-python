from skil import Skil, WorkSpace, Experiment, Model, Deployment
import json

# Initialize a new experiment in a workspace
skil_server = Skil()
ws = WorkSpace(skil_server)
experiment = Experiment(ws)
deployment = Deployment(skil_server)

# Deploy all models with SKIL
skil_services = []
for epoch in range(2):
    model_name = 'model_{epoch:02d}.hdf5'.format(epoch=epoch + 1)
    model = Model(model_name, model_id=epoch, experiment=experiment)
    service = model.deploy(start_server=False, deployment=deployment)
    skil_services.append(service)

# Serve the best one
with open('history.json', 'r') as f:
    history = json.loads(f.read())
    acc = history.get('val_acc')
best_service = skil_services[acc.index(max(acc))]
best_service.start()
