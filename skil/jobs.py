    # @Parameter(names = {"-tm", "--trainingMaster"}, description = "The training master config json file path (local)", arity = 1)
    # private String trainingMasterConfUri = null;

    # @Parameter(names = {"--configPath"}, description = "The path to the config to run.", arity = 1)
    # private String configPath = null;

    # @Parameter(names = {"-ui", "--uiUrl"}, description = "The host:port pair to the ui", arity = 1)
    # private String uiUrl = null;

    # @Parameter(names = {"--evalDataSetProviderClass"}, description = " the evaluation data set provider .", arity = 1)
    # private String evalDataSetProviderClass = "MnistProvider";

    # @Parameter(names = "--pArgs", description = "program arguments")
    # private String pArgs;

    # @Parameter(names = "--modelHistoryUrl", description = "The model history url. Specify the full url (http://someurl:port")
    # private String modelHistoryUrl = null;

    # @Parameter(names = "--modelHistoryId", description = "The model history id")
    # private String modelHistoryId = null;

    # @Parameter(names = "--modelInstanceId", description = "The model instance id")
    # private String modelInstanceId = null;

    # @Parameter(names = "--evalType", description = "The eval type. Possible values: evaluation,evaluationbinary,roc,rocbinary,rocmulticlass,regressionevaluation")
    # private String evalType = null;

 
class InferenceJobConfiguration:

    # TODO signature to aim for: 
    # (experiment, data_path (what), data_format (how), storage_id (where), compute_id)
    # TODO: data format may eventually even be inferred.

    # TODO: we could even consider *setting* compute and storage resources for workspaces
    #       or experiments. No need to specify this every time. 
    def __init__(self, compute_resource_id, storage_resource_id,
                 model_path,  # TODO if we link this to an experiment, this can go
                 batch_size,  # TODO this should either be known to the model or the data, I don't believe this.
                 data_set_provider_class, # TODO: this is an abomination. kill with fire
                 is_multi_data_set=False, # TODO There must be a way to hide this.
                 output_path=None, # TODO: provide a smart default relative to input data or model path.
                 verbose=False):
        self.is_inference = True


class TrainingJobConfiguration:

    def __init__(self, compute_resource_id, storage_resource_id,
                 model_path,
                 num_epochs,
                 data_set_provider_class,
                 eval_data_set_provider_class, # good lord
                 training_master, # TODO: the training master config should be deconstructed. maybe provide this to the job.run(...) as argument.
                 eval_type, # TODO: make this a proper class instead of (or additionally to) strings. TODO: allow multiple eval metrics?!
                 is_multi_data_set=False,
                 output_path=None,
                 ui_url, # TODO: user should just be handed a ui, not take care of url. 
                 verbose=False):
        self.is_inference=False

class Job:

    def __init__(self):
        pass