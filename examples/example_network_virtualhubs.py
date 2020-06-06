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
VIRTUAL_HUB_NAME = "myVirtualHub"
VIRTUAL_WAN_NAME = "myVirtualWan"


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
# /VirtualWans/put/VirtualWANCreate[put]
#--------------------------------------------------------------------------
print("VirtualWANCreate")
BODY = {
  "location": AZURE_LOCATION,
  "tags": {
    "key1": "value1"
  },
  "disable_vpn_encryption": False,
  "type": "Basic"
}
result = mgmt_client.virtual_wans.create_or_update(resource_group_name=RESOURCE_GROUP, virtual_wan_name=VIRTUAL_WAN_NAME, wan_parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /VirtualHubs/put/VirtualHubPut[put]
#--------------------------------------------------------------------------
print("VirtualHubPut")
BODY = {
  "location": AZURE_LOCATION,
  "tags": {
    "key1": "value1"
  },
  "virtual_wan": {
    "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualWans/" + VIRTUAL_WAN_NAME
  },
  "address_prefix": "10.168.0.0/24",
  "sku": "Basic"
}
result = mgmt_client.virtual_hubs.create_or_update(resource_group_name=RESOURCE_GROUP, virtual_hub_name=VIRTUAL_HUB_NAME, virtual_hub_parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /VirtualHubs/get/VirtualHubGet[get]
#--------------------------------------------------------------------------
print("VirtualHubGet")
result = mgmt_client.virtual_hubs.get(resource_group_name=RESOURCE_GROUP, virtual_hub_name=VIRTUAL_HUB_NAME)


#--------------------------------------------------------------------------
# /VirtualHubs/get/VirtualHubListByResourceGroup[get]
#--------------------------------------------------------------------------
print("VirtualHubListByResourceGroup")
result = mgmt_client.virtual_hubs.list_by_resource_group(resource_group_name=RESOURCE_GROUP)


#--------------------------------------------------------------------------
# /VirtualHubs/get/VirtualHubList[get]
#--------------------------------------------------------------------------
print("VirtualHubList")
result = mgmt_client.virtual_hubs.list()


#--------------------------------------------------------------------------
# /VirtualHubs/patch/VirtualHubUpdate[patch]
#--------------------------------------------------------------------------
print("VirtualHubUpdate")
TAGS = {
  "key1": "value1",
  "key2": "value2"
}
result = mgmt_client.virtual_hubs.update_tags(resource_group_name=RESOURCE_GROUP, virtual_hub_name=VIRTUAL_HUB_NAME, tags=TAGS)


#--------------------------------------------------------------------------
# /VirtualHubs/delete/VirtualHubDelete[delete]
#--------------------------------------------------------------------------
print("VirtualHubDelete")
result = mgmt_client.virtual_hubs.delete(resource_group_name=RESOURCE_GROUP, virtual_hub_name=VIRTUAL_HUB_NAME)
result = result.result()
