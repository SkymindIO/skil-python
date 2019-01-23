# SKIL: Deep learning model lifecycle management for humans

[![Build Status](https://jenkins.ci.skymind.io/buildStatus/icon?job=skymind/skil-python/master)](https://jenkins.ci.skymind.io/blue/organizations/jenkins/skymind%2Fskil-python/activity)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/SkymindIO/skil-python/blob/master/LICENSE)
[![PyPI version](https://badge.fury.io/py/skil.svg)](https://badge.fury.io/py/skil)

## Python client for Skymind's intelligence layer (SKIL)

SKIL is an end-to-end deep learning platform. Think of it as a unified front-end for your deep learning training and deployment process. SKIL supports many popular deep learning libraries, such as Keras, TensorFlow and Deeplearning4J. SKIL increases time-to-value of your AI applications by closing the common gap between experiments and production - bringing models to production fast and keeping them there. acting as middleware for all your AI applications. SKIL effectively acts as middleware for your AI applications and solves a range of common _production_ problems of, namely:

- Install and run anywhere: SKIL integrates with your current cloud provider, custom on-premise solutions and hybrid architectures.
- Easy distributed training on Spark: Bring your Keras or TensorFlow model and train it on Apache Spark without any overhead. We support a wide variety of distributed data sources and other vital parts of your production stack.
- Seamless deployment process:  With SKIL, your company's machine learning product lifecycle can be as quick as your data scientist’s experimentation cycle. If you set up a SKIL experiment, model deployment is already accounted for, and makes product integration of deep learning models into a production-grade model server simple - batteries included.
- Built-in reproducibility and compliance: What model and data did you use? Which pre-processing steps were done? Who carried out the experiment? What library versions were used? Which hardware was utilized? SKIL keeps track of all this information for you.
- Model organisation and versioning: SKIL makes it easy to keep your various experiments organised, without interfering with your workflow. Your models are versioned and can be updated at any point.
- Keep working as you're used to: SKIL does not impose an entirely new workflow on you or force you into a UI, just stay right where you are. Happy with your experiment and want to deploy it? Tell SKIL to deploy a service. Your prototype works and you want to scale out training with Spark? Tell SKIL to run a training job.

## Installation

To install SKIL itself, head over to [skymind.ai](https://docs.skymind.ai/docs/installation). Probably the easiest way to get started is by using [docker](https://www.docker.com/):

```bash
docker pull skymindops/skil-ce
docker run --rm -it -p 9008:9008 skymindops/skil-ce bash /start-skil.sh
```

SKIL's Python client can be installed from PyPI:

```bash
pip install skil
```

## Getting started: Deploying an object detection app with SKIL in 60 seconds

We're going to deploy an object detection model pre-trained with Google TensorFlow. The model we use
is the second version of the _You Only Look Once_ (YOLOv2) model trained on the COCO dataset. Download this model from [here](https://github.com/deeplearning4j/dl4j-test-resources/blob/master/src/main/resources/tf_graphs/examples/yolov2_608x608/frozen_model.pb) and store it as `yolo.pb`. If you haven't done already, install and start SKIL as described in the last section.

For this quick example you only need three (self-explanatory) concepts from SKIL. You first create a `Model` from the model file `yolo.pb` you just downloaded. This `Model` becomes a SKIL `Service` by deploying it to a SKIL `Deployment`. That's all there is to it:

```python
import skil

model = skil.Model('yolo.pb', model_id='yolo_42', name='yolo')
service = model.deploy(skil.Deployment(), input_names=['input'], output_names=['output'])
```

Your YOLO object detection app is now live and you can send images to it using the `detect_objects` method of your `service`. We use [OpenCV](https://opencv.org/) (imported as `cv2` into Python) to load, annotate and write images:

```python
import cv2

image = cv2.imread("say_yolo_again.jpg")
detection = service.detect_objects(image)
image = skil.utils.yolo.annotate_image(image, detection)
cv2.imwrite('annotated.jpg', image)
```

This completes your very first SKIL example, but there are many more advanced examples to get you started:

- [Running YOLO against a live web cam](https://github.com/SkymindIO/skil-python/blob/master/examples/tensorflow-yolo/yolo_skil_web_cam.py)
- [Deploying a Keras model as prediction service to SKIL](https://github.com/SkymindIO/skil-python/tree/master/examples/keras-mnist-mlp)
- [Deploying a TensorFlow model as prediction service to SKIL](https://github.com/SkymindIO/skil-python/tree/master/examples/tensorflow-mnist-mlp)
- [Using SKIL's CLI to quickly configure models and deployments](https://github.com/SkymindIO/skil-python/tree/master/examples/skil-cli-keras)
- [Deploying a Keras model from a jupyter notebook](https://github.com/SkymindIO/skil-python/blob/master/examples/keras-skil-example.ipynb)
- [WIP Run a Spark training job from a simple Keras model](https://github.com/SkymindIO/skil-python/tree/master/examples/keras-job)
- [WIP Deploy preprocessing steps and a model as a Pipeline service](https://github.com/SkymindIO/skil-python/tree/master/examples/keras-iris-pipeline)
