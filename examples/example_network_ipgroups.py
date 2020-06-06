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
IP_GROUPS_NAME = "myIpGroups"


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
# /IpGroups/put/CreateOrUpdate_IpGroups[put]
#--------------------------------------------------------------------------
print("CreateOrUpdate_IpGroups")
BODY = {
  "tags": {
    "key1": "value1"
  },
  "location": AZURE_LOCATION,
  "ip_addresses": [
    "13.64.39.16/32",
    "40.74.146.80/31",
    "40.74.147.32/28"
  ]
}
result = mgmt_client.ip_groups.create_or_update(resource_group_name=RESOURCE_GROUP, ip_groups_name=IP_GROUPS_NAME, parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /IpGroups/get/Get_IpGroups[get]
#--------------------------------------------------------------------------
print("Get_IpGroups")
result = mgmt_client.ip_groups.get(resource_group_name=RESOURCE_GROUP, ip_groups_name=IP_GROUPS_NAME)


#--------------------------------------------------------------------------
# /IpGroups/get/ListByResourceGroup_IpGroups[get]
#--------------------------------------------------------------------------
print("ListByResourceGroup_IpGroups")
result = mgmt_client.ip_groups.list_by_resource_group(resource_group_name=RESOURCE_GROUP)


#--------------------------------------------------------------------------
# /IpGroups/get/List_IpGroups[get]
#--------------------------------------------------------------------------
print("List_IpGroups")
result = mgmt_client.ip_groups.list()


#--------------------------------------------------------------------------
# /IpGroups/patch/Update_IpGroups[patch]
#--------------------------------------------------------------------------
print("Update_IpGroups")
TAGS = {
  "key1": "value1",
  "key2": "value2"
}
# result = mgmt_client.ip_groups.update_groups(resource_group_name=RESOURCE_GROUP, ip_groups_name=IP_GROUPS_NAME, tags=TAGS)


#--------------------------------------------------------------------------
# /IpGroups/delete/Delete_IpGroups[delete]
#--------------------------------------------------------------------------
print("Delete_IpGroups")
result = mgmt_client.ip_groups.delete(resource_group_name=RESOURCE_GROUP, ip_groups_name=IP_GROUPS_NAME)
result = result.result()
