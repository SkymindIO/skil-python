import pytest
import skil


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


def test_serving():
    ws = _get_ws()
    exp = skil.Experiment(ws)
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


if __name__ == '__main__':
    pytest.main([__file__])
