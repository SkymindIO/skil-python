import pytest
import skil
import uuid

from skil.resources.common import *

_sk = None


def _get_sk():
    global _sk
    if _sk is None:
        _sk = skil.Skil()
    return _sk


def test_s3_resource():
    sk = _get_sk()
    res = skil.resources.storage.S3(sk, "s3" + str(uuid.uuid1())[:6], "test_bucket",
                                    "test_region", "test_credentials")
    res.delete()


def test_hdfs_resource():
    sk = _get_sk()
    res = skil.resources.storage.HDFS(sk, "hdfs" + str(uuid.uuid1())[:6], "test_name_node_host",
                                      42, "test_credentials")
    res.delete()


def test_google_storage_resource():
    sk = _get_sk()
    res = skil.resources.storage.GoogleStorage(sk, "google_storage" + str(uuid.uuid1())[:6],
                                               "test_project_id", "test_bucket_name", "test_credentials")
    res.delete()


def test_azure_storage_resource():
    sk = _get_sk()
    res = skil.resources.storage.AzureStorage(sk, "azure_storage" + str(uuid.uuid1())[:6],
                                              "test_container_name", "test_credentials")
    res.delete()


def test_emr_resource():
    sk = _get_sk()
    res = skil.resources.compute.EMR(sk, "emr" + str(uuid.uuid1())[:6], "test_region",
                                     "test_credential_uri", "test_cluster_id")
    res.delete()


def test_data_proc_resource():
    sk = _get_sk()
    res = skil.resources.compute.DataProc(sk, "data_proc" + str(uuid.uuid1())[:6],
                                          "test_project_id", "test_region", "test_cluster_name", "test_credentials")
    res.delete()


def test_hd_insight_resource():
    sk = _get_sk()
    res = skil.resources.compute.HDInsight(sk, "hd_insight" + str(uuid.uuid1())[:6],
                                           "test_subscription_id", "test_resource_group_name", "test_cluster_name",
                                           "test_credentials")
    res.delete()


def test_yarn_resource():
    sk = _get_sk()
    res = skil.resources.compute.YARN(sk, "yarn" + str(uuid.uuid1())[:6], "test_local_spark_home",
                                      "test_credentials")
    res.delete()


def test_get_resource_by_id():
    sk = _get_sk()
    res = skil.resources.compute.YARN(sk, "yarn" + str(uuid.uuid1())[:6], "test_local_spark_home",
                                      "test_credentials")
    res_id = res.resource_id

    retrieved = get_resource_by_id(sk, res_id)

    assert retrieved.resource_id == res_id
    res.delete()


def test_get_all_resources():
    sk = _get_sk()
    res1 = skil.resources.compute.YARN(sk, "yarn_1" + str(uuid.uuid1())[:6], "test_local_spark_home",
                                       "test_credentials")

    res2 = skil.resources.compute.HDInsight(sk, "hd_insight_1" + str(uuid.uuid1())[:6],
                                            "test_subscription_id", "test_resource_group_name", "test_cluster_name",
                                            "test_credentials")

    res3 = skil.resources.compute.DataProc(sk, "data_proc_1" + str(uuid.uuid1())[:6],
                                           "test_project_id", "test_region", "test_cluster_name", "test_credentials")
    resources = get_all_resources(sk)

    # assert len(resources) == 3
    assert resources[0].resource_id == res1.resource_id
    assert resources[1].resource_id == res2.resource_id
    assert resources[2].resource_id == res3.resource_id

    res1.delete()
    res2.delete()
    res3.delete()


def test_get_resources_by_type():
    sk = _get_sk()

    # YARN, HDInsight, DataProc, EMR : Compute
    # AzureStorage, GoogleStorage, S3, HDFS: Storage

    res1 = skil.resources.compute.YARN(sk, "yarn" + str(uuid.uuid1())[:6], "test_local_spark_home",
                                       "test_credentials")

    res2 = skil.resources.compute.HDInsight(sk, "hd_insight" + str(uuid.uuid1())[:6],
                                            "test_subscription_id", "test_resource_group_name", "test_cluster_name",
                                            "test_credentials")
    res3 = skil.resources.compute.DataProc(sk, "data_proc" + str(uuid.uuid1())[:6],
                                           "test_project_id", "test_region", "test_cluster_name", "test_credentials")

    res4 = skil.resources.compute.EMR(sk, "emr" + str(uuid.uuid1())[:6], "test_region",
                                      "test_credential_uri", "test_cluster_id")

    res5 = skil.resources.storage.AzureStorage(sk, "azure_storage" + str(uuid.uuid1())[:6],
                                               "test_container_name", "test_credentials")

    res6 = skil.resources.storage.GoogleStorage(sk, "google_storage" + str(uuid.uuid1())[:6],
                                                "test_project_id", "test_bucket_name", "test_credentials")

    res7 = skil.resources.storage.S3(sk, "s3" + str(uuid.uuid1())[:6], "test_bucket",
                                     "test_region", "test_credentials")

    res8 = skil.resources.storage.HDFS(sk, "hdfs" + str(uuid.uuid1())[:6], "test_name_node_host",
                                       42, "test_credentials")

    resources = get_resources_by_type(sk, "COMPUTE")
    # assert len(resources) == 4
    assert resources[0].resource_id == res1.resource_id
    assert resources[1].resource_id == res2.resource_id
    assert resources[2].resource_id == res3.resource_id
    assert resources[3].resource_id == res4.resource_id

    resources = get_resources_by_type(sk, "STORAGE")
    # assert len(resources) == 4
    assert resources[0].resource_id == res5.resource_id
    assert resources[1].resource_id == res6.resource_id
    assert resources[2].resource_id == res7.resource_id
    assert resources[3].resource_id == res8.resource_id

    res1.delete()
    res2.delete()
    res3.delete()
    res4.delete()
    res5.delete()
    res6.delete()
    res7.delete()
    res8.delete()


def test_get_resources_by_sub_type():
    sk = _get_sk()

    # YARN, HDInsight, DataProc, EMR : Compute
    # AzureStorage, GoogleStorage, S3, HDFS: Storage

    res1 = skil.resources.compute.YARN(sk, "yarn" + str(uuid.uuid1())[:6], "test_local_spark_home",
                                       "test_credentials")

    res1a = skil.resources.compute.YARN(sk, "yarn" + str(uuid.uuid1())[:6], "test_local_spark_home_a",
                                        "test_credentials_a")

    res2 = skil.resources.compute.HDInsight(sk, "hd_insight" + str(uuid.uuid1())[:6],
                                            "test_subscription_id", "test_resource_group_name", "test_cluster_name",
                                            "test_credentials")
    res3 = skil.resources.compute.DataProc(sk, "data_proc" + str(uuid.uuid1())[:6],
                                           "test_project_id", "test_region", "test_cluster_name", "test_credentials")

    res4 = skil.resources.compute.EMR(sk, "emr" + str(uuid.uuid1())[:6], "test_region",
                                      "test_credential_uri", "test_cluster_id")

    res5 = skil.resources.storage.AzureStorage(sk, "azure_storage" + str(uuid.uuid1())[:6],
                                               "test_container_name", "test_credentials")

    res6 = skil.resources.storage.GoogleStorage(sk, "google_storage" + str(uuid.uuid1())[:6],
                                                "test_project_id", "test_bucket_name", "test_credentials")

    res7 = skil.resources.storage.S3(sk, "s3" + str(uuid.uuid1())[:6], "test_bucket",
                                     "test_region", "test_credentials")

    res8 = skil.resources.storage.HDFS(sk, "hdfs" + str(uuid.uuid1())[:6], "test_name_node_host",
                                       42, "test_credentials")

    resources = get_resources_by_sub_type(sk, "YARN")
    assert len(resources) == 2
    assert resources[0].resource_id == res1.resource_id
    assert resources[1].resource_id == res1a.resource_id

    resources = get_resources_by_sub_type(sk, "HDInsight")
    assert len(resources) == 1
    assert resources[0].resource_id == res2.resource_id

    resources = get_resources_by_sub_type(sk, "DataProc")
    assert len(resources) == 1
    assert resources[0].resource_id == res3.resource_id

    resources = get_resources_by_sub_type(sk, "EMR")
    assert len(resources) == 1
    assert resources[0].resource_id == res4.resource_id

    resources = get_resources_by_sub_type(sk, "AzureStorage")
    assert len(resources) == 1
    assert resources[0].resource_id == res5.resource_id

    resources = get_resources_by_sub_type(sk, "GoogleStorage")
    assert len(resources) == 1
    assert resources[0].resource_id == res6.resource_id

    resources = get_resources_by_sub_type(sk, "S3")
    assert len(resources) == 1
    assert resources[0].resource_id == res7.resource_id

    resources = get_resources_by_sub_type(sk, "HDFS")
    assert len(resources) == 1
    assert resources[0].resource_id == res8.resource_id

    res1.delete()
    res1a.delete()
    res2.delete()
    res3.delete()
    res4.delete()
    res5.delete()
    res6.delete()
    res7.delete()
    res8.delete()


def test_get_yarn_details_by_id():
    sk = _get_sk()

    res = skil.resources.compute.YARN(sk, "yarn" + str(uuid.uuid1())[:6], "test_local_spark_home",
                                      "test_credentials")
    obj = get_resource_details_by_id(sk, res.resource_id)

    assert obj.resource_id == res.resource_id
    assert obj.name == res.name
    assert obj.local_spark_home == res.local_spark_home

    res.delete()


def test_get_hdinsight_details_by_id():
    sk = _get_sk()
    res = skil.resources.compute.HDInsight(sk, "hd_insight" + str(uuid.uuid1())[:6],
                                           "test_subscription_id", "test_resource_group_name", "test_cluster_name",
                                           "test_credentials")

    obj = get_resource_details_by_id(sk, res.resource_id)

    assert obj.resource_id == res.resource_id
    assert obj.name == res.name
    assert obj.resource_group_name == res.resource_group_name
    assert obj.cluster_name == res.cluster_name
    assert obj.subscription_id == res.subscription_id

    res.delete()


def test_get_azure_storage_details_by_id():
    sk = _get_sk()
    res = skil.resources.storage.AzureStorage(sk, "azure_storage" + str(uuid.uuid1())[:6],
                                              "test_container_name", "test_credentials")

    obj = get_resource_details_by_id(sk, res.resource_id)

    assert obj.resource_id == res.resource_id
    assert obj.name == res.name
    assert obj.container_name == res.container_name

    res.delete()


def test_get_dataproc_details_by_id():
    sk = _get_sk()
    res = skil.resources.compute.DataProc(sk, "data_proc" + str(uuid.uuid1())[:6],
                                          "test_project_id", "test_region", "test_cluster_name", "test_credentials")

    obj = get_resource_details_by_id(sk, res.resource_id)

    assert obj.resource_id == res.resource_id
    assert obj.name == res.name
    assert obj.project_id == res.project_id
    assert obj.cluster_name == res.cluster_name
    assert obj.region == res.region

    res.delete()


def test_get_emr_details_by_id():
    sk = _get_sk()
    res = skil.resources.compute.EMR(sk, "emr" + str(uuid.uuid1())[:6], "test_region",
                                     "test_credential_uri", "test_cluster_id")

    obj = get_resource_details_by_id(sk, res.resource_id)

    assert obj.resource_id == res.resource_id
    assert obj.name == res.name
    assert obj.cluster_id == res.cluster_id
    assert obj.region == res.region

    res.delete()


def test_get_google_storage_details_by_id():
    sk = _get_sk()
    res = skil.resources.storage.GoogleStorage(sk, "google_storage" + str(uuid.uuid1())[:6],
                                               "test_project_id", "test_bucket_name", "test_credentials")

    obj = get_resource_details_by_id(sk, res.resource_id)

    assert obj.resource_id == res.resource_id
    assert obj.name == res.name
    assert obj.project_id == res.project_id
    assert obj.bucket_name == res.bucket_name

    res.delete()


def test_get_s3_details_by_id():
    sk = _get_sk()
    res = skil.resources.storage.S3(sk, "s3" + str(uuid.uuid1())[:6], "test_bucket",
                                    "test_region", "test_credentials")

    obj = get_resource_details_by_id(sk, res.resource_id)

    assert obj.resource_id == res.resource_id
    assert obj.name == res.name
    assert obj.region == res.region
    assert obj.bucket == res.bucket

    res.delete()


def test_get_hdfs_details_by_id():
    sk = _get_sk()
    res = skil.resources.storage.HDFS(sk, "hdfs" + str(uuid.uuid1())[:6], "test_name_node_host",
                                      '42', "test_credentials")

    obj = get_resource_details_by_id(sk, res.resource_id)

    assert obj.resource_id == res.resource_id
    assert obj.name == res.name
    assert obj.name_node_host == res.name_node_host
    assert obj.name_node_port == res.name_node_port

    res.delete()


if __name__ == '__main__':
    pytest.main([__file__])
