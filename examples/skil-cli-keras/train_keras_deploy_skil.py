#!/usr/bin/env python
import keras
from keras.datasets import mnist
from keras.models import Model
from keras.layers import Dense, Dropout, Input

import uuid
from six.moves import range
import numpy as np
from skil import Experiment, Deployment, Model as SkilModel

(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = x_train.reshape(60000, 784)
x_test = x_test.reshape(10000, 784)
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255

num_classes = 10
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

# history = model.fit(x_train, y_train,
#                     batch_size=128,
#                     epochs=10,
#                     verbose=1,
#                     validation_data=(x_test, y_test))
_, acc = model.evaluate(x_test, y_test)


# Load the experiment from file (alternatively create one with Experiment())
# Make sure to run: "pyskil init-experiment -f exp.json" before
experiment = Experiment.load('exp.json')

# Save the model to SKIL
skil_model = SkilModel(model, experiment=experiment)
    
# Add accuracy as evaluation metric to SKIL
skil_model.add_evaluation(accuracy=acc, name="MNIST test set")

# Load the deployment from file (or create one with Deployment()) and deploy model as service
# Make sure to run: "pyskil init-deployment -f dep.json" before
deployment = Deployment.load('dep.json')
service = skil_model.deploy(deployment=deployment)

# Evaluate from scratch, using SKIL
num_correct = 0
for i in range(10000):
    result = service.predict_single(x_test[i])
    num_correct += np.argmax(result) == np.argmax(y_test[i])
print("Test Accuracy: %s" % (float(num_correct) / 10000,))