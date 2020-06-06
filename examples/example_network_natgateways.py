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
NAT_GATEWAY_NAME = "myNatGateway"
PUBLIC_IP_ADDRESS_NAME = "myPublicIpAddress"
PUBLIC_IPPREFIX_NAME = "myPublicIpprefix"
PUBLIC_IP_PREFIX_NAME = "myPublicIpPrefix"


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
# /PublicIPAddresses/put/Create public IP address defaults[put]
#--------------------------------------------------------------------------
print("Create public IP address defaults")
BODY = {
  "location": AZURE_LOCATION,
  "sku": {
    "name": "Standard"
  },
  "public_ip_allocation_method": "Static"
}
result = mgmt_client.public_ip_addresses.create_or_update(resource_group_name=RESOURCE_GROUP, public_ip_address_name=PUBLIC_IP_ADDRESS_NAME, parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /PublicIPPrefixes/put/Create public IP prefix defaults[put]
#--------------------------------------------------------------------------
print("Create public IP prefix defaults")
BODY = {
  "location": AZURE_LOCATION,
  "sku": {
    "name": "Standard"
  },
  "prefix_length": "30"
}
result = mgmt_client.public_ip_prefixes.create_or_update(resource_group_name=RESOURCE_GROUP, public_ip_prefix_name=PUBLIC_IP_PREFIX_NAME, parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /NatGateways/put/Create nat gateway[put]
#--------------------------------------------------------------------------
print("Create nat gateway")
BODY = {
  "location": AZURE_LOCATION,
  "sku": {
    "name": "Standard"
  },
  "public_ip_addresses": [
    {
      "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/publicIPAddresses/" + PUBLIC_IP_ADDRESS_NAME
    }
  ],
  "public_ip_prefixes": [
    {
      "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/publicIPPrefixes/" + PUBLIC_IPPREFIX_NAME
    }
  ]
}
result = mgmt_client.nat_gateways.create_or_update(resource_group_name=RESOURCE_GROUP, nat_gateway_name=NAT_GATEWAY_NAME, parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /NatGateways/get/Get nat gateway[get]
#--------------------------------------------------------------------------
print("Get nat gateway")
result = mgmt_client.nat_gateways.get(resource_group_name=RESOURCE_GROUP, nat_gateway_name=NAT_GATEWAY_NAME)


#--------------------------------------------------------------------------
# /NatGateways/get/List nat gateways in resource group[get]
#--------------------------------------------------------------------------
print("List nat gateways in resource group")
result = mgmt_client.nat_gateways.list(resource_group_name=RESOURCE_GROUP)


#--------------------------------------------------------------------------
# /NatGateways/get/List all nat gateways[get]
#--------------------------------------------------------------------------
print("List all nat gateways")
result = mgmt_client.nat_gateways.list_all()


#--------------------------------------------------------------------------
# /NatGateways/patch/Update nat gateway tags[patch]
#--------------------------------------------------------------------------
print("Update nat gateway tags")
TAGS = {
  "tag1": "value1",
  "tag2": "value2"
}
result = mgmt_client.nat_gateways.update_tags(resource_group_name=RESOURCE_GROUP, nat_gateway_name=NAT_GATEWAY_NAME, tags=TAGS)


#--------------------------------------------------------------------------
# /NatGateways/delete/Delete nat gateway[delete]
#--------------------------------------------------------------------------
print("Delete nat gateway")
result = mgmt_client.nat_gateways.delete(resource_group_name=RESOURCE_GROUP, nat_gateway_name=NAT_GATEWAY_NAME)
result = result.result()
