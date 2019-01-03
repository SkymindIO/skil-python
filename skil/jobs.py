import skil_client


class JobConfiguration:
    """JobConfiguration

    A SKIL job configuration collects all data needed to set up and run a SKIL Job.
    SKIL currently has inference and training jobs, each come with their respective
    configuration.

    # Arguments:
        skil_model: a `skil.Model` instance
        compute_resource: `skil.resources.compute.ComputeResource' instance, created before running a job.
        storage_resource: `skil.resources.storage.StorageResource` instance created before runnning a job.
        output_path: string with path to folder in which job output should be stored.
        data_set_provider_class: name of the class to be used as `DataSetProvider` in SKIL
        is_multi_data_set: boolean, whether data set uses `MultiDataSet` interface.
        verbose: boolean, log level. Set True for detailed logging.

    """

    # TODO: provide a smart default for output_path relative to input data or model path.

    def __init__(self, skil_model, compute_resource, storage_resource,
                 output_path, data_set_provider_class,
                 is_multi_data_set, verbose):
        self.model = skil_model
        self.compute_id = compute_resource.resource_id
        self.storage_id = storage_resource.resource_id
        self.output_path = output_path
        self.dsp = data_set_provider_class
        self.mds = is_multi_data_set
        self.verbose = verbose


class InferenceJobConfiguration(JobConfiguration):
    """InferenceJobConfiguration

    Configuration for a SKIL inference job. On top of what you need to specify for a base JobConfiguration,
    you need to set the batch size for the model as well.

    # Arguments:
        skil_model: a `skil.Model` instance
        batch_size: int, data batch size to run inference with on the model.
        compute_resource: `skil.resources.compute.ComputeResource' instance, created before running a job.
        storage_resource: `skil.resources.storage.StorageResource` instance created before runnning a job
        output_path: string with path to folder in which job output should be stored.
        data_set_provider_class: name of the class to be used as `DataSetProvider` in SKIL
        is_multi_data_set: boolean, whether data set uses `MultiDataSet` interface.
        verbose: boolean, log level. Set True for detailed logging.

    """
    # TODO signature to aim for: (model, data_path (what), data_format (how), storage_id (where), compute_id)
    # TODO: data format may eventually even be inferred automatically. no reason not to. we can do so for models.

    # TODO: we could even consider *setting* compute and storage resources for workspaces
    #       or experiments. No need to specify this every time.

    # TODO batch_size should either be known to the model or the data, I don't believe this.
    # TODO KILL DSP!!!1ONE
    # TODO There must be a way to hide is_multi_data_set

    def __init__(self, skil_model, batch_size, compute_resource, storage_resource, output_path,
                 data_set_provider_class,
                 is_multi_data_set=False,
                 verbose=False):
        super(InferenceJobConfiguration, self).__init__(
            skil_model, compute_resource,
            storage_resource, output_path, data_set_provider_class,
            is_multi_data_set, verbose)

        self.batch_size = batch_size


class TrainingJobConfiguration(JobConfiguration):

    """TrainingJobConfiguration

    Configuration for a SKIL training job. On top of what you need to specify for a base JobConfiguration,
    you need to set the number of epochs to train for, a (distributed) training configuration and provide
    information about how to evaluate your model.

    # Arguments:
        skil_model: a `skil.Model` instance
        compute_resource: `skil.resources.compute.ComputeResource' instance, created before running a job.
        storage_resource: `skil.resources.storage.StorageResource` instance created before runnning a job
        output_path: string with path to folder in which job output should be stored.
        data_set_provider_class: name of the class to be used as `DataSetProvider` in SKIL
        is_multi_data_set: boolean, whether data set uses `MultiDataSet` interface.
        verbose: boolean, log level. Set True for detailed logging.
    """
    # TODO signature to aim for: (model, num_epochs, data_path, eval_data_path, eval_types,
    #  data_format, storage_id, compute_id)
    # TODO what if we want to split data on the go. what about validation data? cross validation?
    #  current concept seems insufficient to cover this properly.
    # TODO model_path, config_path, model config path... why both? should be able to guess this
    # TODO model_history_url=None, can we infer this from experiment?
    # TODO model_history_id=None, this is the workspace id
    # TODO model_instance_id=None, is this alternatively to model/config path? don't get it.
    # TODO: eval_type make this a proper class instead of (or additionally to) strings.
    # TODO: allow multiple eval metrics?!
    # TODO: the training master config should be deconstructed. maybe provide this to the job.run(...) as argument.
    # TODO: user should just be *handed* a ui, not take care of a $%$%! URL.

    def __init__(self,  skil_model, num_epochs,
                 eval_type,
                 eval_data_set_provider_class,  # good lord
                 compute_resource, storage_resource,
                 output_path,
                 data_set_provider_class,
                 is_multi_data_set=False,
                 ui_url=None,
                 verbose=False):
        super(TrainingJobConfiguration, self).__init__(
            skil_model, compute_resource,
            storage_resource, output_path, data_set_provider_class,
            is_multi_data_set, verbose)

        self.num_epochs = num_epochs
        self.eval_dsp = eval_data_set_provider_class
        self.eval_type = eval_type
        self.ui_url = ui_url


class TrainingJob:
    """TrainingJob

    Initialize and run a SKIL training job. If a distributed config is provided,
    SKIL will run your model on Spark. Otherwise it will carry out regular training
    on provided resources.

    # Arguments:
        training_config: `TrainingJobConfiguration` instance
        distributed_config: `DistributedConfiguration` instance

    """

    def __init__(self, skil, training_config, distributed_config=None):

        self.skil = skil
        self.training_config = training_config
        self.tm = distributed_config

        training_create_job_request = skil_client.CreateJobRequest(
            compute_resource_id=self.training_config.compute_id,
            storage_resource_id=self.training_config.storage_id,
            job_args=self._training_job_args(),
            output_file_name=self.training_config.output_path
        )

        # TODO: why do we need to specify the training type here if the request already knows it?
        self.skil.api.create_job("TRAINING", training_create_job_request)

    def run(self):
        pass

    def _training_job_args(self):
        tc = self.training_config
        tm = self.tm

        inference = "-i false "
        output = "-o {} ".format(tc.output_path)
        num_epochs = "--batchSize {} ".format(tc.num_epochs)
        model_path = "-mo {} ".format(tc.model.model_path)
        dsp = "-dsp {} ".format(tc.dsp)
        eval_dsp = "--evalDataSetProviderClass {} ".format(tc.eval_dsp)
        eval_type = "--evalType {} ".format(tc.eval_type)
        tm = "-tm {} ".format(tc.tm)
        mds = "--multiDataSet {} ".format(_bool_to_string(tc.mds))
        verbose = "--verbose {} ".format(_bool_to_string(tc.verbose))

        return inference + output + num_epochs + model_path + dsp + \
            eval_dsp + eval_type + tm + mds + verbose


class InferenceJob:

    def __init__(self, skil, inference_config):

        self.skil = skil
        self.inference_config = inference_config

        inference_create_job_request = skil_client.CreateJobRequest(
            compute_resource_id=self.inference_config.compute_id,
            storage_resource_id=self.inference_config.storage_id,
            job_args=self._inference_job_args(),
            output_file_name=self.inference_config.output_path
        )

        self.skil.api.create_job("INFERENCE", inference_create_job_request)

    def run(self):
        pass

    def _inference_job_args(self):
        ic = self.inference_config

        inference = "-i true "
        output = "-o {} ".format(ic.output_path)
        batch_size = "--batchSize {} ".format(ic.batch_size)
        model_path = "-mo {} ".format(ic.model.model_path)
        dsp = "-dsp {} ".format(ic.dsp)
        mds = "--multiDataSet {} ".format(_bool_to_string(ic.mds))
        verbose = "--verbose {} ".format(_bool_to_string(ic.verbose))

        return inference + output + batch_size + model_path + dsp + \
            mds + verbose


def get_job_by_id(skil_server, job_id):
    # TODO is this available?
    pass


def _bool_to_string(bool):
    return "true" if bool else "false"
