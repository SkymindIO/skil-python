import pytest
import skil
import os
import time
from keras.datasets import mnist
from keras.models import Model
from keras.layers import Dense, Dropout, Input

work_space = None  # because number of workspaces is limited
_sk = None


def _get_sk():
    global _sk
    if _sk is None:
        _sk = skil.Skil()
    return _sk


def _get_ws():
    global work_space
    if work_space is not None:
        return work_space
    sk = _get_sk()
    work_space = skil.WorkSpace(sk)
    return work_space


def save_model():
    num_classes = 10

    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    x_train = x_train.reshape(60000, 784)
    x_test = x_test.reshape(10000, 784)
    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    x_train /= 255
    x_test /= 255

    inp = Input((784,))
    x = Dense(512, activation='relu')(inp)
    x = Dropout(0.2)(x)
    x = Dense(512, activation='relu')(x)
    x = Dropout(0.2)(x)
    out = Dense(num_classes, activation='softmax')(x)

    model = Model(inp, out)

    model.compile(loss='categorical_crossentropy',
                  optimizer='sgd', metrics=['accuracy'])

    model.save("model.h5")


def test_serving():
    ws = _get_ws()
    exp = skil.Experiment(ws)
    save_model()
    model = skil.Model('model.h5', experiment=exp)
    dep = skil.Deployment(ws.skil)
    service = model.deploy(dep)
    from keras.datasets import mnist
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_test = x_test.reshape(10000, 784)
    x_test = x_test.astype('float32')
    x_test /= 255
    service.predict_single(x_test[0])
    service.predict(x_test[:10])

    service.stop()
    time.sleep(4)
    with pytest.raises(Exception):
        service.predict(x_test[:10])

    service.start()
    time.sleep(4)
    service.predict(x_test[:10])

    service.delete()
    os.remove('model.h5')


if __name__ == '__main__':
    pytest.main([__file__])
