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
PEERING_NAME = "AzurePrivatePeering"


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
# /ExpressRouteCircuitPeerings/put/Create ExpressRouteCircuit Peerings[put]
#--------------------------------------------------------------------------
print("Create ExpressRouteCircuit Peerings")
BODY = {
  "peer_asn": "200",
  "primary_peer_address_prefix": "192.168.16.252/30",
  "secondary_peer_address_prefix": "192.168.18.252/30",
  "vlan_id": "200"
}
result = mgmt_client.express_route_circuit_peerings.create_or_update(resource_group_name=RESOURCE_GROUP, circuit_name=CIRCUIT_NAME, peering_name=PEERING_NAME, peering_parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /ExpressRouteCircuitPeerings/get/Get ExpressRouteCircuit Peering[get]
#--------------------------------------------------------------------------
print("Get ExpressRouteCircuit Peering")
result = mgmt_client.express_route_circuit_peerings.get(resource_group_name=RESOURCE_GROUP, circuit_name=CIRCUIT_NAME, peering_name=PEERING_NAME)


#--------------------------------------------------------------------------
# /ExpressRouteCircuitPeerings/get/List ExpressRouteCircuit Peerings[get]
#--------------------------------------------------------------------------
print("List ExpressRouteCircuit Peerings")
result = mgmt_client.express_route_circuit_peerings.list(resource_group_name=RESOURCE_GROUP, circuit_name=CIRCUIT_NAME)


#--------------------------------------------------------------------------
# /ExpressRouteCircuitPeerings/delete/Delete ExpressRouteCircuit Peerings[delete]
#--------------------------------------------------------------------------
print("Delete ExpressRouteCircuit Peerings")
result = mgmt_client.express_route_circuit_peerings.delete(resource_group_name=RESOURCE_GROUP, circuit_name=CIRCUIT_NAME, peering_name=PEERING_NAME)
result = result.result()
