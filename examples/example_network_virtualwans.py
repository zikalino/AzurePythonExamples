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
VIRTUAL_WANNAME = "myVirtualWanname"


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
result = mgmt_client.virtual_wans.create_or_update(resource_group_name=RESOURCE_GROUP, virtual_wan_name=VIRTUAL_WANNAME, wan_parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /VirtualWans/get/VirtualWANGet[get]
#--------------------------------------------------------------------------
print("VirtualWANGet")
result = mgmt_client.virtual_wans.get(resource_group_name=RESOURCE_GROUP, virtual_wan_name=VIRTUAL_WANNAME)


#--------------------------------------------------------------------------
# /VirtualWans/get/VirtualWANListByResourceGroup[get]
#--------------------------------------------------------------------------
print("VirtualWANListByResourceGroup")
result = mgmt_client.virtual_wans.list_by_resource_group(resource_group_name=RESOURCE_GROUP)


#--------------------------------------------------------------------------
# /VirtualWans/get/VirtualWANList[get]
#--------------------------------------------------------------------------
print("VirtualWANList")
result = mgmt_client.virtual_wans.list()


#--------------------------------------------------------------------------
# /VirtualWans/patch/VirtualWANUpdate[patch]
#--------------------------------------------------------------------------
print("VirtualWANUpdate")
TAGS = {
  "key1": "value1",
  "key2": "value2"
}
result = mgmt_client.virtual_wans.update_tags(resource_group_name=RESOURCE_GROUP, virtual_wan_name=VIRTUAL_WANNAME, tags=TAGS)


#--------------------------------------------------------------------------
# /VirtualWans/delete/VirtualWANDelete[delete]
#--------------------------------------------------------------------------
print("VirtualWANDelete")
result = mgmt_client.virtual_wans.delete(resource_group_name=RESOURCE_GROUP, virtual_wan_name=VIRTUAL_WANNAME)
result = result.result()
