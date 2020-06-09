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
SERVICE_ENDPOINT_POLICY_DEFINITION_NAME = "myServiceEndpointPolicyDefinition"


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
# /ServiceEndpointPolicies/put/Create service endpoint policy[put]
#--------------------------------------------------------------------------
print("Create service endpoint policy")
BODY = {
  "location": AZURE_LOCATION
}
result = mgmt_client.service_endpoint_policies.create_or_update(resource_group_name=RESOURCE_GROUP, service_endpoint_policy_name=SERVICE_ENDPOINT_POLICY_NAME, parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /ServiceEndpointPolicyDefinitions/put/Create service endpoint policy definition[put]
#--------------------------------------------------------------------------
print("Create service endpoint policy definition")
BODY = {
  "description": "Storage Service EndpointPolicy Definition",
  "service": "Microsoft.Storage",
  "service_resources": [
    "/subscriptions/subid1",
    "/subscriptions/subid1/resourceGroups/storageRg",
    "/subscriptions/subid1/resourceGroups/storageRg/providers/Microsoft.Storage/storageAccounts/stAccount"
  ]
}
result = mgmt_client.service_endpoint_policy_definitions.create_or_update(resource_group_name=RESOURCE_GROUP, service_endpoint_policy_name=SERVICE_ENDPOINT_POLICY_NAME, service_endpoint_policy_definition_name=SERVICE_ENDPOINT_POLICY_DEFINITION_NAME, service_endpoint_policy_definitions=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /ServiceEndpointPolicyDefinitions/get/Get service endpoint definition in service endpoint policy[get]
#--------------------------------------------------------------------------
print("Get service endpoint definition in service endpoint policy")
result = mgmt_client.service_endpoint_policy_definitions.get(resource_group_name=RESOURCE_GROUP, service_endpoint_policy_name=SERVICE_ENDPOINT_POLICY_NAME, service_endpoint_policy_definition_name=SERVICE_ENDPOINT_POLICY_DEFINITION_NAME)


#--------------------------------------------------------------------------
# /ServiceEndpointPolicyDefinitions/get/List service endpoint definitions in service end point policy[get]
#--------------------------------------------------------------------------
print("List service endpoint definitions in service end point policy")
result = mgmt_client.service_endpoint_policy_definitions.list_by_resource_group(resource_group_name=RESOURCE_GROUP, service_endpoint_policy_name=SERVICE_ENDPOINT_POLICY_NAME)


#--------------------------------------------------------------------------
# /ServiceEndpointPolicyDefinitions/delete/Delete service endpoint policy definitions from service endpoint policy[delete]
#--------------------------------------------------------------------------
print("Delete service endpoint policy definitions from service endpoint policy")
result = mgmt_client.service_endpoint_policy_definitions.delete(resource_group_name=RESOURCE_GROUP, service_endpoint_policy_name=SERVICE_ENDPOINT_POLICY_NAME, service_endpoint_policy_definition_name=SERVICE_ENDPOINT_POLICY_DEFINITION_NAME)
result = result.result()
