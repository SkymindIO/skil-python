import skil_client


class JobConfiguration:

    def __init__(self, skil_model, compute_resource_id, 
                 storage_resource_id, output_path, data_set_provider_class,
                 is_multi_data_set, verbose):
        self.model = skil_model
        self.compute_id = compute_resource_id
        self.storage_id = storage_resource_id
        self.output_path = output_path
        self.dsp = data_set_provider_class
        self.mds = is_multi_data_set
        self.verbose = verbose


class InferenceJobConfiguration(JobConfiguration):

    # TODO signature to aim for: 
    # (model, data_path (what), data_format (how), storage_id (where), compute_id)
    # TODO: data format may eventually even be inferred.

    # TODO: we could even consider *setting* compute and storage resources for workspaces
    #       or experiments. No need to specify this every time. 
    def __init__(self, skil_model, batch_size, compute_resource_id, storage_resource_id, output_path,
                #  model_path,  # TODO if we link this to an experiment, this can go
                #  batch_size,  # TODO this should either be known to the model or the data, I don't believe this.
                 data_set_provider_class, # TODO: this is an abomination. kill with fire
                 is_multi_data_set=False, # TODO There must be a way to hide this.
                #  output_path=None, # TODO: provide a smart default relative to input data or model path.
                 verbose=False):
        super(InferenceJobConfiguration, self).__init__(
            skil_model, batch_size, compute_resource_id, 
            storage_resource_id, output_path, data_set_provider_class, 
            is_multi_data_set, verbose)

        self.batch_size = batch_size


class TrainingJobConfiguration(JobConfiguration):

    # TODO signature to aim for: 
    # (model, num_epochs, data_path, eval_data_path, eval_types,
    #  data_format, storage_id, compute_id)
    # TODO what if we want to split data on the go. what about validation data? cross validation?
    # current concept seems insufficient to cover this properly.

    def __init__(self,  skil_model, num_epochs, compute_resource_id, storage_resource_id,
                 output_path,
                #  model_path, # model path
                #  config_path, # TODO model config path... why both? should be able to guess this
                 data_set_provider_class,
                 eval_data_set_provider_class, # good lord
                 training_master_config, # TODO: the training master config should be deconstructed. maybe provide this to the job.run(...) as argument.
                 eval_type, # TODO: make this a proper class instead of (or additionally to) strings. TODO: allow multiple eval metrics?!
                 is_multi_data_set=False,
                #  model_history_url=None,  # TODO can we infer this from experiment?
                #  model_history_id=None, # TODO this is the workspace id
                #  model_instance_id=None, # TODO is this alternatively to model/config path? don't get it.
                 ui_url=None, # TODO: user should just be handed a ui, not take care of url. 
                 verbose=False):
        super(TrainingJobConfiguration, self).__init__(
            skil_model, compute_resource_id, 
            storage_resource_id, output_path, data_set_provider_class, 
            is_multi_data_set, verbose)
        
        self.num_epochs = num_epochs
        self.eval_dsp = eval_data_set_provider_class
        self.eval_type = eval_type
        self.tm = training_master_config


class TrainingJob:

    def __init__(self, skil, training_config):

        self.skil = skil
        self.training_config = training_config

        training_create_job_request = skil_client.CreateJobRequest(
            compute_resource_id=self.training_config.compute_id,
            storage_resource_id=self.training_config.storage_id,
            job_args = self._training_job_args(),
            output_file_name=self.training_config.output_path
        )

        # TODO: why on earth do I need to specify the training type
        # here if the request already knows it?
        self.skil.api.create_job("TRAINING", training_create_job_request)

    def run(self):
        pass

    
    def _training_job_args(self):

        tc = self.training_config

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
            job_args = self._inference_job_args(),
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

def get_job_by_id(skil, job_id):
    pass


def _bool_to_string(bool):
    return "true" if bool else "false"