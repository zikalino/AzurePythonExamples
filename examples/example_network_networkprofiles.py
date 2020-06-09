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
NETWORK_PROFILE_NAME = "myNetworkProfile"
VIRTUAL_NETWORK_NAME = "myVirtualNetwork"
SUBNET_NAME = "mySubnet"


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
# /Subnets/put/Create subnet[put]
#--------------------------------------------------------------------------
print("Create subnet")
BODY = {
  "address_prefix": "10.0.0.0/16"
}
result = mgmt_client.subnets.create_or_update(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME, subnet_name=SUBNET_NAME, subnet_parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /NetworkProfiles/put/Create network profile defaults[put]
#--------------------------------------------------------------------------
print("Create network profile defaults")
BODY = {
  "location": AZURE_LOCATION,
  "container_network_interface_configurations": [
    {
      "name": "eth1",
      "ip_configurations": [
        {
          "name": "ipconfig1",
          "subnet": {
            "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualNetworks/" + VIRTUAL_NETWORK_NAME + "/subnets/" + SUBNET_NAME
          }
        }
      ]
    }
  ]
}
result = mgmt_client.network_profiles.create_or_update(resource_group_name=RESOURCE_GROUP, network_profile_name=NETWORK_PROFILE_NAME, parameters=BODY)


#--------------------------------------------------------------------------
# /NetworkProfiles/get/Get network profile with container network interfaces[get]
#--------------------------------------------------------------------------
print("Get network profile with container network interfaces")
result = mgmt_client.network_profiles.get(resource_group_name=RESOURCE_GROUP, network_profile_name=NETWORK_PROFILE_NAME)


#--------------------------------------------------------------------------
# /NetworkProfiles/get/Get network profile[get]
#--------------------------------------------------------------------------
print("Get network profile")
result = mgmt_client.network_profiles.get(resource_group_name=RESOURCE_GROUP, network_profile_name=NETWORK_PROFILE_NAME)


#--------------------------------------------------------------------------
# /NetworkProfiles/get/List resource group network profiles[get]
#--------------------------------------------------------------------------
print("List resource group network profiles")
result = mgmt_client.network_profiles.list(resource_group_name=RESOURCE_GROUP)


#--------------------------------------------------------------------------
# /NetworkProfiles/get/List all network profiles[get]
#--------------------------------------------------------------------------
print("List all network profiles")
result = mgmt_client.network_profiles.list_all()


#--------------------------------------------------------------------------
# /NetworkProfiles/patch/Update network profile tags[patch]
#--------------------------------------------------------------------------
print("Update network profile tags")
TAGS = {
  "tag1": "value1",
  "tag2": "value2"
}
result = mgmt_client.network_profiles.update_tags(resource_group_name=RESOURCE_GROUP, network_profile_name=NETWORK_PROFILE_NAME, tags=TAGS)


#--------------------------------------------------------------------------
# /NetworkProfiles/delete/Delete network profile[delete]
#--------------------------------------------------------------------------
print("Delete network profile")
result = mgmt_client.network_profiles.delete(resource_group_name=RESOURCE_GROUP, network_profile_name=NETWORK_PROFILE_NAME)
result = result.result()
