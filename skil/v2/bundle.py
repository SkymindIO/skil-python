from .import_model_request import ImportModelRequest
from .inference_verticle_configuration import InferenceVerticleConfiguration
import os
import json
import zipfile


def create_bundle(
               modelFile,
               modelServerInferenceConfig=None,
               importModelRequest=None,
               inferenceVerticleConfiguration=None,
               extraFiles=None,
               outputFile=None
                ):
    if not outputFile:
        outputFile = os.path.abspath("deploymentbundle.zip")

    assert os.path.isfile(modelFile)

    assert isinstance(importModelRequest, ImportModelRequest)
    assert isinstance(inferenceVerticleConfiguration, InferenceVerticleConfiguration)

    if extraFiles is None:
        extraFiles = []
    assert isinstance(extraFiles, list)
    for f in extraFiles:
        assert os.path.isfile(f)

    assert isinstance(outputFile, str)

    if modelServerInferenceConfig is not None:
        inferenceVerticleConfiguration.modelServerInferenceConfig = modelServerInferenceConfig

    files_to_compress = []

    config_file = "config.json"
    import_config_file = "import-config.json"

    with open(config_file, 'w') as f:
        json.dump(inferenceVerticleConfiguration.tojson(), f)
    with open(import_config_file, 'w') as f:
        json.dump(importModelRequest.tojson(), f)

    files_to_compress += extraFiles
    files_to_compress.append(import_config_file)
    files_to_compress.append(config_file)
    files_to_compress.append(modelFile)

    with zipfile.ZipFile(outputFile, 'w') as zf:
        for f in files_to_compress:
            zf.write(f)

    return outputFile
