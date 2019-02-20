import os
import shutil
import sys
import uuid

import keras
from six import text_type as unicode
from six import string_types


class SkilContext(object):
    """SkilContext manages models from within a Zeppelin notebook
    hosted by SKIL. The Spark context necessary for initialization
    is provided in any notebook created with SKIL.

    SkilContext can upload models, add them to an experiment and
    add evaluation metrics to a model.  
    """

    def __init__(self, sc):
        self._sc = sc

        self.JvmSkilContext = sc._jvm.io.skymind.zeppelin.utils.SkilContext
        self._ctx = self.JvmSkilContext()

        self.SKILEnvironment = sc._jvm.io.skymind.skil.service.SKILEnvironment
        self.ModelInstanceEntity = sc._jvm.io.skymind.modelproviders.history.model.ModelInstanceEntity
        self.Nd4j = sc._jvm.org.nd4j.linalg.factory.Nd4j
        self.Evaluation = sc._jvm.org.deeplearning4j.eval.Evaluation

    def _models_path(self):
        service_path = self.SKILEnvironment.skilServiceWorkingDirFile().toString()
        storage_path = os.path.join(service_path, "storage")
        models_path = os.path.join(storage_path, "models")

        if not os.path.exists(storage_path):
            os.mkdir(storage_path)
        if not os.path.exists(models_path):
            os.mkdir(models_path)

        return models_path

    def experiment_id(self, z):
        """Get the experiment ID of the current notebook or None.

        # Arguments:
            z: the ZeppelinContext

        # Return value:
            The experiment ID
        """

        return self._ctx.experimentId(z.z)

    def save_model(self, z, model):
        """Save the model into the managed models directory.

        # Arguments:
            z: The ZeppelinContext
            model: The model to save

        # Return value:
            The path of the saved model.
        """

        experiment_id = self.experiment_id(z)
        if experiment_id is None:
            return None

        if isinstance(model, keras.models.Model):
            models_path = self._models_path()
            file_path = os.path.join(models_path, str(uuid.uuid1()) + '.h5')

            if isinstance(file_path, unicode):
                file_path = file_path.encode(sys.getfilesystemencoding())

            model.save(str(file_path))

            return file_path
        else:
            raise NotImplementedError("Only Keras models currently supported.")

    def copy_model(self, z, source_path, model_type):
        """Copy a model file (tensorflow or ONNX) to the managed model directory.

        # Arguments:
            z: The ZeppelinContext
            path: The path to the model you want to copy
            model_type: The type of model. Currently either 'tensorflow' or 'onnx'

        # Return value:
            The path of the saved model
        """

        models_path = self._models_path()

        if model_type.lower() == 'tensorflow' or model_type.lower() == 'tf':
            dest_path = os.path.join(models_path, str(uuid.uuid1()) + '.pb')
        elif model_type.lower() == 'onnx':
            dest_path = os.path.join(models_path, str(uuid.uuid1()) + '.onnx')
        else:
            raise NotImplementedError(
                'Only TensorFlow and ONNX model types are supported.')

        shutil.copyfile(source_path, dest_path)

        return dest_path

    def add_model_to_experiment(self, z, model, name=None):
        """Add the model to the model list inside the SKIL Experiment.

        # Arguments:
            z: The ZeppelinContext
            model: The model to save or path.
            name: Optional name of the model.

        # Return value:
            The ModelInstanceID for use with adding EvaluationResults.
        """

        model_id = str(uuid.uuid1())
        if isinstance(model, string_types):
            model_path = model
        elif isinstance(model, keras.models.Model):
            model_path = self.save_model(z, model)
        else:
            raise NotImplementedError(
                "Can only auto-save Keras models. For TensorFlow or ONNX models please save them separately.")

        instance = (self.ModelInstanceEntity
                    .builder()
                    .modelName(name)
                    .experimentId(self.experiment_id(z))
                    .modelId(model_id)
                    .created(self._sc._jvm.java.util.Date())
                    .uri('file://' + model_path)
                    .etlJson(None)
                    .notebookJson(None)
                    .build())

        self._ctx.getClient().addModelInstance(instance)

        return model_id

    def add_evaluation_to_model(self, z, model_id, model, data, labels, name=None):
        """Gathers the evalutation results of the model on the specified test data.

        # Arguments:
            z: The ZeppelinContext
            model_id: The ModelInstanceID
            model: The model to use
            data: The dataset to evaluate
            labels: The labels of the dataset
            name: A name for the EvaluationResults

        # Return value:
            The id of the EvaluationResults if saved.
        """

        def assign(np_arr, jvm_arr):
            i = 0
            for row in np_arr.tolist():
                j = 0
                for col in row:
                    jvm_arr[i][j] = col
                    j += 1
                i += 1

        if not isinstance(model, keras.models.Model):
            raise NotImplementedError("Only Keras models currently supported.")

        preds = model.predict(data)
        p_arr = self._sc._gateway.new_array(
            self._sc._gateway.jvm.double, preds.shape[0], preds.shape[1])
        assign(preds, p_arr)
        nd_pred = self.Nd4j.create(p_arr)
        y_arr = self._sc._gateway.new_array(
            self._sc._gateway.jvm.double, labels.shape[0], labels.shape[1])
        assign(labels, y_arr)
        nd_y = self.Nd4j.create(y_arr)

        e = self.Evaluation(int(nd_y.shape()[1]))
        e.eval(nd_y, nd_pred)

        return self._ctx.addEvaluationToModel(z.z, model_id, e, name)

    # Camel case methods for backward compatibility
    def experimentId(self, z):
        return self.experiment_id(z)

    def saveModel(self, z, model):
        return self.save_model(z, model)

    def copyModel(self, z, source_path, model_type):
        return self.copy_model(z, source_path, model_type)

    def addModelToExperiment(self, z, model, name=None):
        return self.add_model_to_experiment(z, model, name)

    def addEvaluationToModel(self, z, model_id, model, data, labels, name=None):
        return self.add_evaluation_to_model(z, model_id, model, data, labels, name)
