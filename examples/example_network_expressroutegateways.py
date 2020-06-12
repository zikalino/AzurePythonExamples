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
VIRTUAL_WAN_NAME = "myVirtualWan"
VIRTUAL_HUB_NAME = "myVirtualHub"
EXPRESS_ROUTE_GATEWAY_NAME = "myExpressRouteGateway"


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
  "type": "Standard"
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
# /ExpressRouteGateways/put/ExpressRouteGatewayCreate[put]
#--------------------------------------------------------------------------
print("ExpressRouteGatewayCreate")
BODY = {
  "location": AZURE_LOCATION,
  "virtual_hub": {
    "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualHubs/" + VIRTUAL_HUB_NAME
  },
  "auto_scale_configuration": {
    "bounds": {
      "min": "3"
    }
  }
}
result = mgmt_client.express_route_gateways.create_or_update(resource_group_name=RESOURCE_GROUP, express_route_gateway_name=EXPRESS_ROUTE_GATEWAY_NAME, put_express_route_gateway_parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /ExpressRouteGateways/get/ExpressRouteGatewayListByResourceGroup[get]
#--------------------------------------------------------------------------
print("ExpressRouteGatewayListByResourceGroup")
result = mgmt_client.express_route_gateways.list_by_resource_group(resource_group_name=RESOURCE_GROUP)


#--------------------------------------------------------------------------
# /ExpressRouteGateways/get/ExpressRouteGatewayListBySubscription[get]
#--------------------------------------------------------------------------
print("ExpressRouteGatewayListBySubscription")
result = mgmt_client.express_route_gateways.list_by_subscription()


#--------------------------------------------------------------------------
# /ExpressRouteGateways/get/ExpressRouteGatewayGet[get]
#--------------------------------------------------------------------------
print("ExpressRouteGatewayGet")
result = mgmt_client.express_route_gateways.get(resource_group_name=RESOURCE_GROUP, express_route_gateway_name=EXPRESS_ROUTE_GATEWAY_NAME)


#--------------------------------------------------------------------------
# /ExpressRouteGateways/delete/ExpressRouteGatewayDelete[delete]
#--------------------------------------------------------------------------
print("ExpressRouteGatewayDelete")
result = mgmt_client.express_route_gateways.delete(resource_group_name=RESOURCE_GROUP, express_route_gateway_name=EXPRESS_ROUTE_GATEWAY_NAME)
result = result.result()
