import skil_client
from .base import Resource


class EMR(Resource):
    """EMR

    AWS Elastic Map Reduce compute resource

    # Arguments:
        skil: `Skil` server instance
        name: Name of the resource
        region: AWS region of the EMR cluster
        credential_uri: path to credential file
        cluster_id: ID of the EMR cluster
        resource_id: optional resource ID to retrieve an existing resource
        create: boolean, for internal use only. whether to create a new resource or not
    """
    # TODO: if cluster_id is None, spin up a cluster and retrieve id (requires work in SKIL core)
    # TODO: can we hide setting credentials? i.e. can these be put into a
    #   little config file (similar to what we do in pydl4j?).

    def __init__(self, skil, name, region, credential_uri, cluster_id=None,
                 resource_id=None, create=True):

        super(EMR, self).__init__(skil)
        self.name = name
        self.region = region
        self.credential_uri = credential_uri
        self.cluster_id = cluster_id
        self.resource_id = resource_id

        if create:
            resource_response = self.skil.api.add_resource(skil_client.AddResourceRequest(
                resource_name=self.name,
                resource_details=skil_client.EMRResourceDetails(
                    cluster_id=self.cluster_id,
                    region=self.region
                ),
                credential_uri=self.credential_uri,
                type="COMPUTE",
                sub_type="EMR")
            )
            self.resource_id = resource_response.get("resourceId")
        else:
            if resource_id is None:
                raise ValueError(
                    'If create is False you need to provide a valid resource_id')


class DataProc(Resource):
    """DataProc

    Google cloud engine DataProc compute resource

    # Arguments:
        skil: `Skil` server instance
        name: Resource name
        project_id: GCE project ID
        region: GCE region
        spark_cluster_name: DataProc cluster name
        credential_uri: path to credential file
        resource_id: optional resource ID to retrieve an existing resource
        create: boolean, for internal use only. whether to create a new resource or not
    """

    def __init__(self, skil, name, project_id, region, spark_cluster_name, credential_uri,
                 resource_id=None, create=True):
        super(DataProc, self).__init__(skil)
        self.name = name
        self.project_id = project_id
        self.region = region
        self.credential_uri = credential_uri
        self.cluster_name = spark_cluster_name
        self.resource_id = resource_id
        if create:
            resource_response = self.skil.api.add_resource(skil_client.AddResourceRequest(
                resource_name=self.name,
                resource_details=skil_client.DataProcResourceDetails(
                    project_id=self.project_id,
                    region=self.region,
                    spark_cluster_name=self.cluster_name
                ),
                credential_uri=self.credential_uri,
                type="COMPUTE",
                sub_type="DataProc")
            )
            self.resource_id = resource_response.get("resourceId")
        else:
            if resource_id is None:
                raise ValueError(
                    'If create is False you need to provide a valid resource_id')


class HDInsight(Resource):
    """HDInsight

    Azure HDInsight compute resource.

    # Arguments:
        skil: `Skil` server instance
        name: Resource name
        subscription_id: Azure subscription ID
        resource_group_name: Azure resource group name
        cluster_name: HDInsight cluster name
        credential_uri: path to credential file
        resource_id: optional resource ID to retrieve an existing resource
        create: boolean, for internal use only. whether to create a new resource or not
    """

    def __init__(self, skil, name, subscription_id, resource_group_name, cluster_name, credential_uri,
                 resource_id=None, create=True):
        super(HDInsight, self).__init__(skil)
        self.name = name
        self.subscription_id = subscription_id
        self.resource_group_name = resource_group_name
        self.cluster_name = cluster_name
        self.credential_uri = credential_uri
        self.resource_id = resource_id

        if create:
            resource_response = self.skil.api.add_resource(skil_client.AddResourceRequest(
                resource_name=self.name,
                resource_details=skil_client.HDInsightResourceDetails(
                    subscription_id=self.subscription_id,
                    resource_group_name=self.resource_group_name,
                    cluster_name=self.cluster_name
                ),
                credential_uri=self.credential_uri,
                type="COMPUTE",
                sub_type="HDInsight")
            )
            self.resource_id = resource_response.get("resourceId")
        else:
            if resource_id is None:
                raise ValueError(
                    'If create is False you need to provide a valid resource_id')


class YARN(Resource):
    """YARN
    YARN compute resource for local Spark computation on YARN.
    # Arguments:
        skil: `Skil` server instance
        name: Resource name
        local_spark_home: full path to local Spark binary
        resource_id: optional resource ID to retrieve an existing resource
        create: boolean, for internal use only. whether to create a new resource or not
    """

    def __init__(self, skil, name, local_spark_home, credential_uri,
                 resource_id=None, create=True):
        super(YARN, self).__init__(skil)
        self.name = name
        self.local_spark_home = local_spark_home
        self.credential_uri = credential_uri
        self.resource_id = resource_id

        if create:
            resource_response = self.skil.api.add_resource(skil_client.AddResourceRequest(
                resource_name=self.name,
                resource_details=skil_client.YARNResourceDetails(
                    local_spark_home=self.local_spark_home
                ),
                credential_uri=self.credential_uri,
                type="COMPUTE",
                sub_type="YARN")
            )
            self.resource_id = resource_response.get("resourceId")
        else:
            if resource_id is None:
                raise ValueError(
                    'If create is False you need to provide a valid resource_id')