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
