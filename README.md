# SKIL: Deep learning model lifecycle management for humans

[![Build Status](https://jenkins.ci.skymind.io/buildStatus/icon?job=skymind/skil-python/master)](https://jenkins.ci.skymind.io/blue/organizations/jenkins/skymind%2Fskil-python/activity)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/SkymindIO/skil-python/blob/master/LICENSE)
[![PyPI version](https://badge.fury.io/py/skil.svg)](https://badge.fury.io/py/skil)

## Python client for Skymind's intelligence layer (SKIL)

SKIL is an end-to-end deep learning platform. Think of it as a unified front-end for your deep learning training and deployment process. SKIL supports many popular deep learning libraries, such as Keras, TensorFlow and Deeplearning4J. SKIL increases time-to-value of your AI applications by closing the common gap between experiments and production - bringing models to production fast and keeping them there. SKIL effectively acts as middleware for your AI applications and solves a range of common _production_ problems, namely:

- _Install and run anywhere_: SKIL integrates with your current cloud provider, custom on-premise solutions and hybrid architectures.
- _Easy distributed training on Spark_: Bring your Keras or TensorFlow model and train it on Apache Spark without any overhead. We support a wide variety of distributed storage and compute resources and can handle all components of your production stack.
- _Seamless deployment process_:  With SKIL, your company's machine learning product lifecycle can be as quick as your data scientist’s experimentation cycle. If you set up a SKIL experiment, model deployment is already accounted for, and makes product integration of deep learning models into a production-grade model server simple - batteries included.
- _Built-in reproducibility and compliance_: What model and data did you use? Which pre-processing steps were done? What library versions were used? Which hardware was utilized? SKIL keeps track of all this information for you.
- _Model organisation and versioning_: SKIL makes it easy to keep your various experiments organised, without interfering with your workflow. Your models are versioned and can be updated at any point.
- _Keep working as you're used to_: SKIL does not impose an entirely new workflow on you, just stay right where you are. Happy with your experiment and want to deploy it? Tell SKIL to deploy a service. Your prototype works and you want to scale out training with Spark? Tell SKIL to run a training job. You have a great model, but massive amounts of data for inference that your model can't process quickly enough? Tell SKIL to run an inference job on Spark.

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

In this section you're going to deploy a state-of-the-art object detection application. As a first step,  download [the TensorFlow model we pre-trained for you](https://github.com/deeplearning4j/dl4j-test-resources/blob/master/src/main/resources/tf_graphs/examples/yolov2_608x608/frozen_model.pb) and store it locally as `yolo.pb`. As the name suggests, this model is a [You Only Look Once (YOLO) model](https://pjreddie.com/darknet/yolo/).If you haven't done already, install and start SKIL as described in the last section.

For this quick example you only need three (self-explanatory) concepts from SKIL. You first create a SKIL `Model` from the model file `yolo.pb` you just downloaded. This `Model` becomes a SKIL `Service` by deploying it to a SKIL `Deployment`. That's all there is to it:

```python
import skil

model = skil.Model('yolo.pb', model_id='yolo_42', name='yolo_model')
service = model.deploy(skil.Deployment(), input_names=['input'], output_names=['output'])
```

Your YOLO object detection app is now live! You can send images to it using the `detect_objects` method of your `service`. We use [OpenCV](https://opencv.org/), imported as `cv2` into Python, to load, annotate and write images. The full example (including model and images) is [located here](https://github.com/SkymindIO/skil-python/tree/master/examples/tensorflow-yolo) for your convenience.

```python
import cv2

image = cv2.imread("say_yolo_again.jpg")
detection = service.detect_objects(image)
image = skil.utils.yolo.annotate_image(image, detection)
cv2.imwrite('annotated.jpg', image)
```

Next, have a look at the SKIL UI at [http://localhost:9008](http://localhost:9008) to see how everything you just did is automatically tracked by SKIL. The UI is mostly self-explanatory and you shouldn't have much trouble navigating it. After logging in (use "admin" as user name and password), you will see that SKIL has created a _workspace_ for you in the "Workspaces" tab. If you click on that workspace, you'll find a so called _experiment_, which contains the yolo model you just loaded into SKIL. Each SKIL experiment comes with a notebook that you can work in. In fact, if you click on "Open notebook" next to the experiment, you will be redirected to a live notebook that contains another interesting example that shows how to deploy Keras and DL4J models (the former in Python, the latter in Scala - all in the same notebook). If you like notebooks and a managed environment that provides you with everything you need out of the box, you can SKIL's notebooks for all your workload. For instance, you could copy and paste the 7 lines of code for the above YOLO app in a SKIL notebook and it will work the same way!

In the "Deployments" tab of the UI, you can see your deployed YOLO service, which consists of just one model, and you'll see that it is "Fully deployed". If you click on the deployment you'll see more details of it, for instance you can explicitly check the endpoints your service is available at. You could, among other things, also re-import the model again through the UI (in case you have a better version or needed to make other changes).

This completes your very first SKIL example, but there are many more advanced examples to get you started:

- [Running YOLO against a live web cam](https://github.com/SkymindIO/skil-python/blob/master/examples/tensorflow-yolo/yolo_skil_web_cam.py)
- [Deploying a Keras model as prediction service to SKIL](https://github.com/SkymindIO/skil-python/tree/master/examples/keras-mnist-mlp)
- [Deploying a TensorFlow model as prediction service to SKIL](https://github.com/SkymindIO/skil-python/tree/master/examples/tensorflow-mnist-mlp)
- [Using SKIL's CLI to quickly configure models and deployments](https://github.com/SkymindIO/skil-python/tree/master/examples/skil-cli-keras)
- [Deploying a Keras model from a jupyter notebook](https://github.com/SkymindIO/skil-python/blob/master/examples/keras-skil-example.ipynb)
- [WIP Run a Spark training job from a simple Keras model](https://github.com/SkymindIO/skil-python/tree/master/examples/keras-job)
- [WIP Deploy preprocessing steps and a model as a Pipeline service](https://github.com/SkymindIO/skil-python/tree/master/examples/keras-iris-pipeline)
