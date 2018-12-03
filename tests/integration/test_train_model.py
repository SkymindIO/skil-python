#!/usr/bin/env python

import os.path

import keras
from keras.datasets import mnist
from keras.models import Model
from keras.layers import Dense, Dropout, Input

import json

import skil
from skil import Skil, WorkSpace, Experiment, Model as SkilModel

import uuid

# Read the SKIL conf and initialize if missing.
skil_conf = None
if not os.path.isfile('.skil'):
    with open('.skil', 'w') as f:
        json.dump({
            'host': 'localhost', # Edit this if using docker-machine.
            'port': '9008',
            'username': 'admin',
            'password': 'admin',
            'workspace_id': '',
            'experiment_id': '',
            'deployment_id': ''
        }, f)

with open('.skil', 'r') as f:
    skil_conf = json.load(f)

# Connect to SKIL and create an experiment for storing our model experiments.
skil_server = Skil(
    host=skil_conf['host'],
    port=skil_conf['port'],
    user_id=skil_conf['username'], 
    password=skil_conf['password'])

work_space = None
if skil_conf['workspace_id'] == '':
    work_space = WorkSpace(skil_server, name="Mnist Sample")
    skil_conf['workspace_id'] = work_space.id
else:
    work_space = skil.get_workspace_by_id(None, skil_server, skil_conf['workspace_id'])

experiment = None
if skil_conf['experiment_id'] == '':
    experiment = Experiment(work_space, name='Simple MLP')
    skil_conf['experiment_id'] = experiment.id
else:
    experiment = skil.get_experiment_by_id(work_space, skil_conf['experiment_id'])

with open('.skil', 'w') as f:
    json.dump(skil_conf, f)

# Train the model.
batch_size = 128
num_classes = 10
epochs = 10

(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = x_train.reshape(60000, 784)
x_test = x_test.reshape(10000, 784)
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255

y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)


inp = Input((784,))
x = Dense(512, activation='relu')(inp)
x = Dropout(0.2)(x)
x = Dense(512, activation='relu')(x)
x = Dropout(0.2)(x)
out = Dense(num_classes, activation='softmax')(x)

model = Model(inp, out)

model.summary()

model.compile(loss='categorical_crossentropy',
              optimizer='sgd', metrics=['accuracy'])


history = model.fit(x_train, y_train,
                    batch_size=batch_size,
                    epochs=epochs,
                    verbose=1,
                    validation_data=(x_test, y_test))

print('Saving model.')

model.save('keras_mnist.h5')

loss, acc = model.evaluate(x_test, y_test)

# Save the model to SKIL with a descriptive name.
skil_model = SkilModel('keras_mnist.h5', 
    id=str(uuid.uuid1()),
    experiment=experiment, 
    name="3-layer MLP with dropout " + str(epochs) + " epochs" )
skil_model.add_evaluation(accuracy=acc, name="MNIST test set")

print('Saved model in SKIL as: ' + skil_model.id)