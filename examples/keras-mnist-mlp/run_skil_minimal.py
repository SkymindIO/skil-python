from skil import Skil, WorkSpace, Experiment, Model, Deployment

skil_server = Skil()
work_space = WorkSpace(skil_server)
experiment = Experiment(work_space)
deployment = Deployment(skil_server, "keras_models")


model_name = 'model_20.hdf5'  # run train.py before
model = Model(model_name, id='model_20', experiment=experiment)
service = model.deploy(start_server=True, deployment=deployment)
