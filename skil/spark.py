import json


class DistributedConfiguration:

    def __init__(self):
        self.config = None

    def to_json(self):
        return json.dumps(self.config)


class ParameterAveraging(DistributedConfiguration):
    def __init__(self, num_workers, batch_size, averaging_frequency=5,
                 num_batches_prefetch=0, collect_stats=False):
        """ParameterAveraging

        # Arguments:
            num_workers: number of Spark workers/executors.
            batch_size: batch size used for model training
            averaging_frequency: int, after how many batches of training averaging takes place
            num_batches_prefetch: int, how many batches to pre-fetch, deactivated if 0.
            collect_stats: boolean, if statistics get collected during training
         """
        self.config = {
            'numWorkers': num_workers,
            'batchSize': batch_size,
            'averagingFrequency': averaging_frequency,
            'numBatchesPrefetch': num_batches_prefetch,
            'collectStats': collect_stats
        }


class ParameterSharing(DistributedConfiguration):
    def __init__(self, num_workers, batch_size,
                 shake_frequency=0, min_threshold=1e-5, update_threshold=1e-3, workers_per_node=-1,
                 num_batches_prefetch=0, step_delay=50, step_trigger=0.05, threshold_step=1e-5,
                 collect_stats=False):
        """ParameterSharing
            num_workers: number of Spark workers/executors.
            batch_size: batch size used for model training
            shake_frequency: shake frequency
            min_threshold: minimum threshold
            update_threshold: update threshold
            workers_per_node: workers per node
            num_batches_prefetch: number of batches to prefetch
            step_delay: step delay
            step_trigger: step trigger
            threshold_step: threshold step
            collect_stats: boolean, if statistics get collected during training
        """
        self.config = {
            'numWorkers': num_workers,
            'batchSize': batch_size,
            'shakeFrequency': shake_frequency,
            'minThreshold': min_threshold,
            'updateThreshold': update_threshold,
            'workersPerNode': workers_per_node,
            'numBatchesPrefetch': num_batches_prefetch,
            'stepDelay': step_delay,
            'thresholdStep': threshold_step,
            'collectStats': collect_stats
        }
