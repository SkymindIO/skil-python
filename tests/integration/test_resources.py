import pytest
import skil
import uuid


_sk = None


def _get_sk():
    global _sk
    if _sk is None:
        _sk = skil.Skil()
    return _sk


def test_s3_resource():
    sk = _get_sk()
    res = skil.resources.storage.S3(sk, "s3" + str(uuid.uuid1)[:6], "test_bucket",
                                    "test_region", "test_credentials")
    res.delete()


def test_hdfs_resource():
    sk = _get_sk()
    res = skil.resources.storage.HDFS(sk, "hdfs" + str(uuid.uuid1)[:6], "test_name_node_host",
                                      42, "test_credentials")
    res.delete()


def test_google_storage_resource():
    sk = _get_sk()
    res = skil.resources.storage.GoogleStorage(sk, "google_storage" + str(uuid.uuid1)[:6],
                                               "test_project_id", "test_bucket_name", "test_credentials")
    res.delete()


def test_azure_storage_resource():
    sk = _get_sk()
    res = skil.resources.storage.AzureStorage(sk, "azure_storage" + str(uuid.uuid1)[:6],
                                              "test_container_name", "test_credentials")
    res.delete()


def test_emr_resource():
    sk = _get_sk()
    res = skil.resources.compute.EMR(sk, "emr" + str(uuid.uuid1)[:6], "test_region",
                                     "test_credential_uri", "test_cluster_id")
    res.delete()


def test_data_proc_resource():
    sk = _get_sk()
    res = skil.resources.compute.DataProc(sk, "data_proc" + str(uuid.uuid1)[:6],
                                          "test_project_id", "test_region", "test_cluster_name", "test_credentials")
    res.delete()


def test_hd_insight_resource():
    sk = _get_sk()
    res = skil.resources.compute.HDInsight(sk, "hd_insight" + str(uuid.uuid1)[:6],
                                           "test_subscription_id", "test_resource_group_name", "test_cluster_name",
                                           "test_credentials")
    res.delete()


def test_yarn_resource():
    sk = _get_sk()
    res = skil.resources.compute.YARN(sk, "yarn" + str(uuid.uuid1)[:6], "test_local_spark_home",
                                      "test_credentials")
    res.delete()


if __name__ == '__main__':
    pytest.main([__file__])
