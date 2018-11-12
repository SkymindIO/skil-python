import pytest
import skil


_sk = None


def _get_sk():
    global _sk
    if _sk is None:
        _sk = skil.Skil()
    return _sk


def test_s3_resource():
    sk = _get_sk()
    res = skil.resources.storage.S3(sk, "s3", "test_bucket", "test_region")
    res.delete()


def test_hdfs_resource():
    sk = _get_sk()
    res = skil.resources.storage.HDFS(sk, "hdfs", "test_name_node_host", "test_name_node_port")
    res.delete()


def test_google_storage_resource():
    sk = _get_sk()
    res = skil.resources.storage.GoogleStorage(sk, "google_storage", "test_project_id", "test_bucket_name")
    res.delete()


def test_azure_storage_resource():
    sk = _get_sk()
    res = skil.resources.storage.AzureStorage(sk, "azure_storage", "test_container_name")
    res.delete()


def test_emr_resource():
    sk = _get_sk()
    res = skil.resources.compute.EMR(sk, "emr", "test_region", "test_credential_uri", "test_cluster_id")
    res.delete()


def test_data_proc_resource():
    sk = _get_sk()
    res = skil.resources.compute.EMR(sk, "data_proc", "test_region", "test_credential_uri", "test_cluster_id")
    res.delete()


def test_hd_insight_resource():
    sk = _get_sk()
    res = skil.resources.compute.HDInsight(sk, "hd_insight", "test_subscription_id", "test_resource_group_name", "test_cluster_name")
    res.delete()


def test_yarn_resource():
    sk = _get_sk()
    res = skil.resources.compute.YARN(sk, "yarn", "test_local_spark_home")
    res.delete()


if __name__ == '__main__':
    pytest.main([__file__])
