from keras.layers import Dense
from keras.models import Sequential
import pytest
import skil
import skil_client
import os
import time


def _get_iris_model():
    model = Sequential()
    model.add(Dense(10, input_dim=4, activation="tanh"))
    model.add(Dense(3, activation="softmax"))

    model.compile(loss="mse", optimizer="sgd")
    path = "model.h5"
    model.save(path)
    return path


def _get_iris_input_schema():
    schema = skil.v2.Schema()
    schema.add_string("petal_length")
    schema.add_string("petal_width")
    schema.add_string("sepal_width")
    schema.add_string("sepal_hright")
    return schema


def _get_iris_output_schema():
    schema = skil.v2.Schema()
    schema.add_double("setosa")
    schema.add_double("versicolor")
    schema.add_double("virginica")
    return schema


def test_model_server_v2():
    # Create V2 bundle:
    modelFile = _get_iris_model()

    modelServerInferenceConfig = skil.v2.ModelServerInferenceConfig.defaultConfig()

    modelConfigType = skil.v2.ModelConfigType(modelLoadingPath="",
                                              outputAdapterType=skil.v2.OutputAdapterType.CLASSIFICATION,
                                              modelType=skil.v2.ModelType.KERAS)

    modelLoadingConfig = skil.v2.ModelLoadingConfig([modelConfigType])

    configuration = skil.v2.InferenceVerticleConfiguration(inputDataType=skil.v2.InputDataType.JSON,
                                                           inferenceLoadingConfigKey=modelServerInferenceConfig,
                                                           outputsKey=_get_iris_output_schema(),
                                                           modelLoadingConfig=modelLoadingConfig,
                                                           schemaKey=_get_iris_input_schema())

    importModelRequest = skil.v2.ImportModelRequest(fileLocation="model.h5",
                                                    modelServerV2ConfigFileLocation="",
                                                    name="testmodel",
                                                    scale=1,
                                                    uri=[],
                                                    modelType="modelv2",
                                                    )
    
    deployment_bundle = skil.v2.create_bundle(modelFile=modelFile,
                                              modelServerInferenceConfig=modelServerInferenceConfig,
                                              importModelRequest=importModelRequest,
                                              inferenceVerticleConfiguration=configuration)

    assert os.path.isfile(deployment_bundle)

    sk = skil.Skil(password="adminadmin")
    sk.upload_model(deployment_bundle)
    importModelRequest2 = skil_client.ImportModelRequest(file_location=sk.get_model_path(deployment_bundle),
                                                         name="testmodel",
                                                         scale=1,
                                                         model_type="modelv2",
                                                         uri=[],
                                                         )
    deployment = skil.Deployment(sk)
    sk.api.deploy_model(deployment.id, importModelRequest2)
    # V2 model deployed

    # Start service:
    model_entity = sk.api.models(deployment.id)[0]
    sk.api.model_state_change(deployment.id,
                              model_entity.id,
                              skil_client.SetState("start"))

    sk.printer.pprint("Starting service...")
    while True:
        time.sleep(2)
        model_state = sk.api.model_state_change(deployment.id,
                                                model_entity.id,
                                                skil_client.SetState("start")).state
        if model_state == "started":
            sk.printer.pprint("Model Server V2 started successfully!")
            break
        else:
            sk.printer.pprint(".")

    # Service started

    # Do inference:

    






if __name__ == '__main__':
    pytest.main([__file__])
