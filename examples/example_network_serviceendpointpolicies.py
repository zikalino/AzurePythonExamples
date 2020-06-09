#-------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#--------------------------------------------------------------------------

import os
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.common.credentials import ServicePrincipalCredentials


#--------------------------------------------------------------------------
# credentials from environment
#--------------------------------------------------------------------------
SUBSCRIPTION_ID = os.environ['AZURE_SUBSCRIPTION_ID']
TENANT_ID = os.environ['AZURE_TENANT']
CLIENT_ID = os.environ['AZURE_CLIENT_ID']
CLIENT_SECRET = os.environ['AZURE_SECRET']


#--------------------------------------------------------------------------
# variables
#--------------------------------------------------------------------------
AZURE_LOCATION = 'eastus'
RESOURCE_GROUP = "myResourceGroup"
SERVICE_ENDPOINT_POLICY_NAME = "myServiceEndpointPolicy"


#--------------------------------------------------------------------------
# management clients
#--------------------------------------------------------------------------
credentials = ServicePrincipalCredentials(
    client_id=CLIENT_ID,
    secret=CLIENT_SECRET,
    tenant=TENANT_ID
)
mgmt_client = NetworkManagementClient(credentials, SUBSCRIPTION_ID)
resource_client = ResourceManagementClient(credentials, SUBSCRIPTION_ID)


#--------------------------------------------------------------------------
# resource group (prerequisite)
#--------------------------------------------------------------------------
print("Creating Resource Group")
resource_client.resource_groups.create_or_update(resource_group_name=RESOURCE_GROUP, parameters={ 'location': AZURE_LOCATION })


#--------------------------------------------------------------------------
# /ServiceEndpointPolicies/put/Create service endpoint policy with definition[put]
#--------------------------------------------------------------------------
print("Create service endpoint policy with definition")
BODY = {
  "location": AZURE_LOCATION,
  "service_endpoint_policy_definitions": [
    {
      "name": "StorageServiceEndpointPolicyDefinition",
      "description": "Storage Service EndpointPolicy Definition",
      "service": "Microsoft.Storage",
      "service_resources": [
        "/subscriptions/subid1",
        "/subscriptions/subid1/resourceGroups/storageRg",
        "/subscriptions/subid1/resourceGroups/storageRg/providers/Microsoft.Storage/storageAccounts/stAccount"
      ]
    }
  ]
}
result = mgmt_client.service_endpoint_policies.create_or_update(resource_group_name=RESOURCE_GROUP, service_endpoint_policy_name=SERVICE_ENDPOINT_POLICY_NAME, parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /ServiceEndpointPolicies/put/Create service endpoint policy[put]
#--------------------------------------------------------------------------
print("Create service endpoint policy")
BODY = {
  "location": AZURE_LOCATION
}
result = mgmt_client.service_endpoint_policies.create_or_update(resource_group_name=RESOURCE_GROUP, service_endpoint_policy_name=SERVICE_ENDPOINT_POLICY_NAME, parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /ServiceEndpointPolicies/get/Get service endPoint Policy[get]
#--------------------------------------------------------------------------
print("Get service endPoint Policy")
result = mgmt_client.service_endpoint_policies.get(resource_group_name=RESOURCE_GROUP, service_endpoint_policy_name=SERVICE_ENDPOINT_POLICY_NAME)


#--------------------------------------------------------------------------
# /ServiceEndpointPolicies/get/List resource group service endpoint policies[get]
#--------------------------------------------------------------------------
print("List resource group service endpoint policies")
result = mgmt_client.service_endpoint_policies.list_by_resource_group(resource_group_name=RESOURCE_GROUP)


#--------------------------------------------------------------------------
# /ServiceEndpointPolicies/get/List all service endpoint policy[get]
#--------------------------------------------------------------------------
print("List all service endpoint policy")
result = mgmt_client.service_endpoint_policies.list()


#--------------------------------------------------------------------------
# /ServiceEndpointPolicies/patch/Update service endpoint policy tags[patch]
#--------------------------------------------------------------------------
print("Update service endpoint policy tags")
TAGS = {
  "tag1": "value1",
  "tag2": "value2"
}
result = mgmt_client.service_endpoint_policies.update_tags(resource_group_name=RESOURCE_GROUP, service_endpoint_policy_name=SERVICE_ENDPOINT_POLICY_NAME, tags=TAGS)


#--------------------------------------------------------------------------
# /ServiceEndpointPolicies/delete/Delete service endpoint policy[delete]
#--------------------------------------------------------------------------
print("Delete service endpoint policy")
result = mgmt_client.service_endpoint_policies.delete(resource_group_name=RESOURCE_GROUP, service_endpoint_policy_name=SERVICE_ENDPOINT_POLICY_NAME)
result = result.result()
