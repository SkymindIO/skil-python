import json
import yaml


def serialize_config(config, file_name, file_format):
    """ Serialize a configuration object to a file in a provided
    file format.

    # Arguments:
        config: Python dictionary with fields to serialize
        file_name: file name in your local file system to store configuration to
        file_format: supported file format, choose from 'json' and 'yaml'
    """
    with open(file_name, 'w') as f:
        if file_format == 'json':
            json.dump(config, f)
        elif file_format == 'yaml':
            yaml.dump(config, f)
        else:
            raise Exception("Unsupported file format {}".format(file_format))


def deserialize_config(file_name):
    """ Deserialize a Python dictionary from file. Tries to infer
    the file format. Handles 'yaml' and 'json' file formats.

    # Arguments:
        file_name: file name in your local file system to load configuration from
    """
    with open(file_name, 'r') as f:
        try:
            result = yaml.load(f)
        except:
            raise Exception(
                'Could not infer file format. Did you serialize your object as "yaml" or "json"?')
        if not hasattr(result, 'keys'):
            raise Exception(
                'Could not infer file format. Did you serialize your object as "yaml" or "json"?')
        return result
