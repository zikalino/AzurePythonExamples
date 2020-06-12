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
AUTHORIZATION_NAME = "myAuthorization"


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
# /ExpressRouteCircuitAuthorizations/put/Create ExpressRouteCircuit Authorization[put]
#--------------------------------------------------------------------------
print("Create ExpressRouteCircuit Authorization")
BODY = {}
result = mgmt_client.express_route_circuit_authorizations.create_or_update(resource_group_name=RESOURCE_GROUP, circuit_name=CIRCUIT_NAME, authorization_name=AUTHORIZATION_NAME, authorization_parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /ExpressRouteCircuitAuthorizations/get/Get ExpressRouteCircuit Authorization[get]
#--------------------------------------------------------------------------
print("Get ExpressRouteCircuit Authorization")
result = mgmt_client.express_route_circuit_authorizations.get(resource_group_name=RESOURCE_GROUP, circuit_name=CIRCUIT_NAME, authorization_name=AUTHORIZATION_NAME)


#--------------------------------------------------------------------------
# /ExpressRouteCircuitAuthorizations/get/List ExpressRouteCircuit Authorization[get]
#--------------------------------------------------------------------------
print("List ExpressRouteCircuit Authorization")
result = mgmt_client.express_route_circuit_authorizations.list(resource_group_name=RESOURCE_GROUP, circuit_name=CIRCUIT_NAME)


#--------------------------------------------------------------------------
# /ExpressRouteCircuitAuthorizations/delete/Delete ExpressRouteCircuit Authorization[delete]
#--------------------------------------------------------------------------
print("Delete ExpressRouteCircuit Authorization")
result = mgmt_client.express_route_circuit_authorizations.delete(resource_group_name=RESOURCE_GROUP, circuit_name=CIRCUIT_NAME, authorization_name=AUTHORIZATION_NAME)
result = result.result()
