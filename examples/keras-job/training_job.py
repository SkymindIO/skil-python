import skil
from keras.models import model_from_config
import json

# Load Keras model you want to train
with open('keras_config.json', 'r') as f:
    model = model_from_config(json.load(f))
    model.compile(loss='categorical_crossentropy', optimizer='sgd')

# Create a SKIL model from it
skil_server = skil.Skil()
ws = skil.WorkSpace(skil_server)
experiment = skil.Experiment(ws)
model = skil.Model(model, model_id='keras_mnist_mlp_42', name='keras', experiment=experiment)

# Register compute and storage resources.
s3 = skil.resources.storage.S3(skil_server, 's3_resource', 'bucket_name', 'region')
emr = skil.resources.compute.EMR(skil_server, 'emr_cluster', 'region', 'credential_uri', 'cluster_id')

# Define your general training setup
training_config = skil.jobs.TrainingJobConfiguration(
    skil_model=model, num_epochs=10, eval_type='ROC_MULTI_CLASS',
    storage_resource=s3,compute_resource=emr,
    data_set_provider_class='MnistProvider', 
    eval_data_set_provider_class='MnistProvider',
    output_path='.')

# Optionally specify a distributed training config.
distributed_config = skil.spark.ParameterSharing(num_workers=8, batch_size=16)

# Create and run a training job.
job = skil.jobs.TrainingJob(skil_server, training_config, distributed_config)
job.run()