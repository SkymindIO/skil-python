from skil import Skil, get_service_by_id, Service

skil_server = Skil()

# Use your previously created SKIL entity IDs
experiment_id = 'your_experiment_id'
model_id = 'your_model_id'
deployment_id = 'your_deployment_id'

service = get_service_by_id(
    skil_server,
    experiment_id,
    model_id,
    deployment_id)

# Note that you can also save and load services,
# which might be more convenient in practice.

service.save('my_service.json')

recovered_service = Service.load('my_service.json')

# You can now predict etc. as before.