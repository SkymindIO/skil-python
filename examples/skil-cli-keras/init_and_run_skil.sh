#!/usr/bin/bash
pyskil init-experiment -f exp.json
pyskil init-deployment -f dep.json

python train_keras_deploy_skil.py