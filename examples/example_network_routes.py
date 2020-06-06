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
ROUTE_TABLE_NAME = "myRouteTable"
ROUTE_NAME = "myRoute"


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
# /RouteTables/put/Create route table[put]
#--------------------------------------------------------------------------
print("Create route table")
BODY = {
  "location": AZURE_LOCATION
}
result = mgmt_client.route_tables.create_or_update(resource_group_name=RESOURCE_GROUP, route_table_name=ROUTE_TABLE_NAME, parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /Routes/put/Create route[put]
#--------------------------------------------------------------------------
print("Create route")
BODY = {
  "address_prefix": "10.0.3.0/24",
  "next_hop_type": "VirtualNetworkGateway"
}
result = mgmt_client.routes.create_or_update(resource_group_name=RESOURCE_GROUP, route_table_name=ROUTE_TABLE_NAME, route_name=ROUTE_NAME, route_parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /Routes/get/Get route[get]
#--------------------------------------------------------------------------
print("Get route")
result = mgmt_client.routes.get(resource_group_name=RESOURCE_GROUP, route_table_name=ROUTE_TABLE_NAME, route_name=ROUTE_NAME)


#--------------------------------------------------------------------------
# /Routes/get/List routes[get]
#--------------------------------------------------------------------------
print("List routes")
result = mgmt_client.routes.list(resource_group_name=RESOURCE_GROUP, route_table_name=ROUTE_TABLE_NAME)


#--------------------------------------------------------------------------
# /Routes/delete/Delete route[delete]
#--------------------------------------------------------------------------
print("Delete route")
result = mgmt_client.routes.delete(resource_group_name=RESOURCE_GROUP, route_table_name=ROUTE_TABLE_NAME, route_name=ROUTE_NAME)
result = result.result()
