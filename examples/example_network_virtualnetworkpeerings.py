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
VIRTUAL_NETWORK_NAME = "myVirtualNetwork"
VIRTUAL_NETWORK_NAME_2 = "myVirtualNetwork2"
VIRTUAL_NETWORK_PEERING_NAME = "myVirtualNetworkPeering"


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
# /VirtualNetworks/put/Create virtual network[put]
#--------------------------------------------------------------------------
print("Create virtual network")
BODY = {
  "location": AZURE_LOCATION,
  "address_space": {
    "address_prefixes": [
      "10.0.0.0/16"
    ]
  }
}
result = mgmt_client.virtual_networks.create_or_update(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME, parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /VirtualNetworks/put/Create virtual network[put]
#--------------------------------------------------------------------------
print("Create virtual network")
BODY = {
  "location": AZURE_LOCATION,
  "address_space": {
    "address_prefixes": [
      "10.1.0.0/16"
    ]
  }
}
result = mgmt_client.virtual_networks.create_or_update(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME_2, parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /VirtualNetworkPeerings/put/Create peering[put]
#--------------------------------------------------------------------------
print("Create peering")
BODY = {
  "allow_virtual_network_access": True,
  "allow_forwarded_traffic": True,
  "allow_gateway_transit": False,
  "use_remote_gateways": False,
  "remote_virtual_network": {
    "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualNetworks/" + VIRTUAL_NETWORK_NAME_2
  }
}
result = mgmt_client.virtual_network_peerings.create_or_update(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME, virtual_network_peering_name=VIRTUAL_NETWORK_PEERING_NAME, virtual_network_peering_parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /VirtualNetworkPeerings/get/Get peering[get]
#--------------------------------------------------------------------------
print("Get peering")
result = mgmt_client.virtual_network_peerings.get(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME, virtual_network_peering_name=VIRTUAL_NETWORK_PEERING_NAME)


#--------------------------------------------------------------------------
# /VirtualNetworkPeerings/get/List peerings[get]
#--------------------------------------------------------------------------
print("List peerings")
result = mgmt_client.virtual_network_peerings.list(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME)


#--------------------------------------------------------------------------
# /VirtualNetworkPeerings/delete/Delete peering[delete]
#--------------------------------------------------------------------------
print("Delete peering")
result = mgmt_client.virtual_network_peerings.delete(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME, virtual_network_peering_name=VIRTUAL_NETWORK_PEERING_NAME)
result = result.result()
