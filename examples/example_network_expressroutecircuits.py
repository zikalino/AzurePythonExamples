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
CIRCUIT_NAME = "myCircuit"
EXPRESS_ROUTE_PORT_NAME = "myExpressRoutePort"
PEERING_NAME = "myPeering"
DEVICE_PATH = "myDevicePath"


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
# /ExpressRouteCircuits/put/Create ExpressRouteCircuit[put]
#--------------------------------------------------------------------------
print("Create ExpressRouteCircuit")
BODY = {
  "sku": {
    "name": "Standard_MeteredData",
    "tier": "Standard",
    "family": "MeteredData"
  },
  "location": AZURE_LOCATION,
  "authorizations": [],
  "peerings": [],
  "allow_classic_operations": False,
  "service_provider_properties": {
    "service_provider_name": "Equinix",
    "peering_location": "Silicon Valley",
    "bandwidth_in_mbps": "200"
  }
}
result = mgmt_client.express_route_circuits.create_or_update(resource_group_name=RESOURCE_GROUP, circuit_name=CIRCUIT_NAME, parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /ExpressRouteCircuits/put/Create ExpressRouteCircuit on ExpressRoutePort[put]
#--------------------------------------------------------------------------
print("Create ExpressRouteCircuit on ExpressRoutePort")
BODY = {
  "location": AZURE_LOCATION,
  "sku": {
    "name": "Premium_MeteredData",
    "tier": "Premium",
    "family": "MeteredData"
  },
  "express_route_port": {
    "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/expressRoutePorts/" + EXPRESS_ROUTE_PORT_NAME
  },
  "bandwidth_in_gbps": "10"
}
#result = mgmt_client.express_route_circuits.create_or_update(resource_group_name=RESOURCE_GROUP, circuit_name=CIRCUIT_NAME, parameters=BODY)
#result = result.result()


#--------------------------------------------------------------------------
# /ExpressRouteCircuits/get/Get ExpressRoute Circuit Peering Traffic Stats[get]
#--------------------------------------------------------------------------
print("Get ExpressRoute Circuit Peering Traffic Stats")
#result = mgmt_client.express_route_circuits.get_peering_stats(resource_group_name=RESOURCE_GROUP, circuit_name=CIRCUIT_NAME, peering_name=PEERING_NAME)


#--------------------------------------------------------------------------
# /ExpressRouteCircuits/get/Get ExpressRoute Circuit Traffic Stats[get]
#--------------------------------------------------------------------------
print("Get ExpressRoute Circuit Traffic Stats")
result = mgmt_client.express_route_circuits.get_stats(resource_group_name=RESOURCE_GROUP, circuit_name=CIRCUIT_NAME)


#--------------------------------------------------------------------------
# /ExpressRouteCircuits/get/Get ExpressRouteCircuit[get]
#--------------------------------------------------------------------------
print("Get ExpressRouteCircuit")
result = mgmt_client.express_route_circuits.get(resource_group_name=RESOURCE_GROUP, circuit_name=CIRCUIT_NAME)


#--------------------------------------------------------------------------
# /ExpressRouteCircuits/get/List ExpressRouteCircuits in a resource group[get]
#--------------------------------------------------------------------------
print("List ExpressRouteCircuits in a resource group")
result = mgmt_client.express_route_circuits.list(resource_group_name=RESOURCE_GROUP)


#--------------------------------------------------------------------------
# /ExpressRouteCircuits/get/List ExpressRouteCircuits in a subscription[get]
#--------------------------------------------------------------------------
print("List ExpressRouteCircuits in a subscription")
result = mgmt_client.express_route_circuits.list_all()


#--------------------------------------------------------------------------
# /ExpressRouteCircuits/post/List Route Table Summary[post]
#--------------------------------------------------------------------------
print("List Route Table Summary")
#result = mgmt_client.express_route_circuits.list_routes_table_summary(resource_group_name=RESOURCE_GROUP, circuit_name=CIRCUIT_NAME, peering_name=PEERING_NAME, device_path=DEVICE_PATH)
#result = result.result()


#--------------------------------------------------------------------------
# /ExpressRouteCircuits/post/List Route Tables[post]
#--------------------------------------------------------------------------
print("List Route Tables")
#result = mgmt_client.express_route_circuits.list_routes_table(resource_group_name=RESOURCE_GROUP, circuit_name=CIRCUIT_NAME, peering_name=PEERING_NAME, device_path=DEVICE_PATH)
#result = result.result()


#--------------------------------------------------------------------------
# /ExpressRouteCircuits/post/List ARP Table[post]
#--------------------------------------------------------------------------
print("List ARP Table")
#result = mgmt_client.express_route_circuits.list_arp_table(resource_group_name=RESOURCE_GROUP, circuit_name=CIRCUIT_NAME, peering_name=PEERING_NAME, device_path=DEVICE_PATH)
#result = result.result()


#--------------------------------------------------------------------------
# /ExpressRouteCircuits/patch/Update Express Route Circuit Tags[patch]
#--------------------------------------------------------------------------
print("Update Express Route Circuit Tags")
TAGS = {
  "tag1": "value1",
  "tag2": "value2"
}
result = mgmt_client.express_route_circuits.update_tags(resource_group_name=RESOURCE_GROUP, circuit_name=CIRCUIT_NAME, tags=TAGS)


#--------------------------------------------------------------------------
# /ExpressRouteCircuits/delete/Delete ExpressRouteCircuit[delete]
#--------------------------------------------------------------------------
print("Delete ExpressRouteCircuit")
#result = mgmt_client.express_route_circuits.delete(resource_group_name=RESOURCE_GROUP, circuit_name=CIRCUIT_NAME)
#result = result.result()
