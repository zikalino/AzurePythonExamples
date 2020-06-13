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
DDOS_CUSTOM_POLICY_NAME = "myDdosCustomPolicy"


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
# No region enabled
# /DdosCustomPolicies/put/Create DDoS custom policy[put]
#--------------------------------------------------------------------------
print("Create DDoS custom policy")
BODY = {
  "location": AZURE_LOCATION,
  "protocol_custom_settings": [
    {
      "protocol": "Tcp"
    }
  ]
}
# result = mgmt_client.ddos_custom_policies.create_or_update(resource_group_name=RESOURCE_GROUP, ddos_custom_policy_name=DDOS_CUSTOM_POLICY_NAME, parameters=BODY)
# result = result.result()


#--------------------------------------------------------------------------
# No region enabled
# /DdosCustomPolicies/get/Get DDoS custom policy[get]
#--------------------------------------------------------------------------
print("Get DDoS custom policy")
# result = mgmt_client.ddos_custom_policies.get(resource_group_name=RESOURCE_GROUP, ddos_custom_policy_name=DDOS_CUSTOM_POLICY_NAME)


#--------------------------------------------------------------------------
# No region enabled
# /DdosCustomPolicies/patch/DDoS Custom policy Update tags[patch]
#--------------------------------------------------------------------------
print("DDoS Custom policy Update tags")
TAGS = {
  "tag1": "value1",
  "tag2": "value2"
}
# result = mgmt_client.ddos_custom_policies.update_tags(resource_group_name=RESOURCE_GROUP, ddos_custom_policy_name=DDOS_CUSTOM_POLICY_NAME, tags=TAGS)


#--------------------------------------------------------------------------
# No region enabled
# /DdosCustomPolicies/delete/Delete DDoS custom policy[delete]
#--------------------------------------------------------------------------
print("Delete DDoS custom policy")
# result = mgmt_client.ddos_custom_policies.delete(resource_group_name=RESOURCE_GROUP, ddos_custom_policy_name=DDOS_CUSTOM_POLICY_NAME)
# result = result.result()
