from skil import Skil, WorkSpace, Experiment, Model, Deployment
from keras.datasets import mnist
import os

model_path = os.path.join('model', 'model.pb')

skil_server = Skil()
work_space = WorkSpace(skil_server)
experiment = Experiment(work_space)
model = Model(model_path, experiment=experiment)

deployment = Deployment(skil_server, "tf_model")
service = model.deploy(deployment)


(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_test = x_test.reshape(10000, 784)
x_test = x_test.astype('float32')
x_test /= 255

print(service.predict_single(x_test[0]))
print(service.predict(x_test[:10]))
