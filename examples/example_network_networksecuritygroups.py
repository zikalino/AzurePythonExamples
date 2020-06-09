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
NETWORK_SECURITY_GROUP_NAME = "myNetworkSecurityGroup"


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
# /NetworkSecurityGroups/put/Create network security group[put]
#--------------------------------------------------------------------------
print("Create network security group")
BODY = {
  "location": AZURE_LOCATION
}
result = mgmt_client.network_security_groups.create_or_update(resource_group_name=RESOURCE_GROUP, network_security_group_name=NETWORK_SECURITY_GROUP_NAME, parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /NetworkSecurityGroups/put/Create network security group with rule[put]
#--------------------------------------------------------------------------
print("Create network security group with rule")
BODY = {
  "location": AZURE_LOCATION,
  "security_rules": [
    {
      "name": "rule1",
      "protocol": "*",
      "source_address_prefix": "*",
      "destination_address_prefix": "*",
      "access": "Allow",
      "destination_port_range": "80",
      "source_port_range": "*",
      "priority": "130",
      "direction": "Inbound"
    }
  ]
}
result = mgmt_client.network_security_groups.create_or_update(resource_group_name=RESOURCE_GROUP, network_security_group_name=NETWORK_SECURITY_GROUP_NAME, parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /NetworkSecurityGroups/get/Get network security group[get]
#--------------------------------------------------------------------------
print("Get network security group")
result = mgmt_client.network_security_groups.get(resource_group_name=RESOURCE_GROUP, network_security_group_name=NETWORK_SECURITY_GROUP_NAME)


#--------------------------------------------------------------------------
# /NetworkSecurityGroups/get/List network security groups in resource group[get]
#--------------------------------------------------------------------------
print("List network security groups in resource group")
result = mgmt_client.network_security_groups.list(resource_group_name=RESOURCE_GROUP)


#--------------------------------------------------------------------------
# /NetworkSecurityGroups/get/List all network security groups[get]
#--------------------------------------------------------------------------
print("List all network security groups")
result = mgmt_client.network_security_groups.list_all()


#--------------------------------------------------------------------------
# /NetworkSecurityGroups/patch/Update network security group tags[patch]
#--------------------------------------------------------------------------
print("Update network security group tags")
TAGS = {
  "tag1": "value1",
  "tag2": "value2"
}
result = mgmt_client.network_security_groups.update_tags(resource_group_name=RESOURCE_GROUP, network_security_group_name=NETWORK_SECURITY_GROUP_NAME, tags=TAGS)


#--------------------------------------------------------------------------
# /NetworkSecurityGroups/delete/Delete network security group[delete]
#--------------------------------------------------------------------------
print("Delete network security group")
result = mgmt_client.network_security_groups.delete(resource_group_name=RESOURCE_GROUP, network_security_group_name=NETWORK_SECURITY_GROUP_NAME)
result = result.result()
