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
LOCAL_NETWORK_GATEWAY_NAME = "myLocalNetworkGateway"


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
# /LocalNetworkGateways/put/CreateLocalNetworkGateway[put]
#--------------------------------------------------------------------------
print("CreateLocalNetworkGateway")
BODY = {
  "location": AZURE_LOCATION,
  "local_network_address_space": {
    "address_prefixes": [
      "10.1.0.0/16"
    ]
  },
  # "gateway_ip_address": "11.12.13.14",
  "fqdn": "site1.contoso.com"
}
result = mgmt_client.local_network_gateways.create_or_update(resource_group_name=RESOURCE_GROUP, local_network_gateway_name=LOCAL_NETWORK_GATEWAY_NAME, parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /LocalNetworkGateways/get/GetLocalNetworkGateway[get]
#--------------------------------------------------------------------------
print("GetLocalNetworkGateway")
result = mgmt_client.local_network_gateways.get(resource_group_name=RESOURCE_GROUP, local_network_gateway_name=LOCAL_NETWORK_GATEWAY_NAME)


#--------------------------------------------------------------------------
# /LocalNetworkGateways/get/ListLocalNetworkGateways[get]
#--------------------------------------------------------------------------
print("ListLocalNetworkGateways")
result = mgmt_client.local_network_gateways.list(resource_group_name=RESOURCE_GROUP)


#--------------------------------------------------------------------------
# /LocalNetworkGateways/patch/UpdateLocalNetworkGatewayTags[patch]
#--------------------------------------------------------------------------
print("UpdateLocalNetworkGatewayTags")
TAGS = {
  "tag1": "value1",
  "tag2": "value2"
}
result = mgmt_client.local_network_gateways.update_tags(resource_group_name=RESOURCE_GROUP, local_network_gateway_name=LOCAL_NETWORK_GATEWAY_NAME, tags=TAGS)


#--------------------------------------------------------------------------
# /LocalNetworkGateways/delete/DeleteLocalNetworkGateway[delete]
#--------------------------------------------------------------------------
print("DeleteLocalNetworkGateway")
result = mgmt_client.local_network_gateways.delete(resource_group_name=RESOURCE_GROUP, local_network_gateway_name=LOCAL_NETWORK_GATEWAY_NAME)
result = result.result()
