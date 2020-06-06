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
# /RouteTables/put/Create route table with route[put]
#--------------------------------------------------------------------------
print("Create route table with route")
BODY = {
  "disable_bgp_route_propagation": True,
  "routes": [
    {
      "name": "route1",
      "address_prefix": "10.0.3.0/24",
      "next_hop_type": "VirtualNetworkGateway"
    }
  ],
  "location": AZURE_LOCATION
}
result = mgmt_client.route_tables.create_or_update(resource_group_name=RESOURCE_GROUP, route_table_name=ROUTE_TABLE_NAME, parameters=BODY)
result = result.result()


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
# /RouteTables/get/Get route table[get]
#--------------------------------------------------------------------------
print("Get route table")
result = mgmt_client.route_tables.get(resource_group_name=RESOURCE_GROUP, route_table_name=ROUTE_TABLE_NAME)


#--------------------------------------------------------------------------
# /RouteTables/get/List route tables in resource group[get]
#--------------------------------------------------------------------------
print("List route tables in resource group")
result = mgmt_client.route_tables.list(resource_group_name=RESOURCE_GROUP)


#--------------------------------------------------------------------------
# /RouteTables/get/List all route tables[get]
#--------------------------------------------------------------------------
print("List all route tables")
result = mgmt_client.route_tables.list_all()


#--------------------------------------------------------------------------
# /RouteTables/patch/Update route table tags[patch]
#--------------------------------------------------------------------------
print("Update route table tags")
TAGS = {
  "tag1": "value1",
  "tag2": "value2"
}
result = mgmt_client.route_tables.update_tags(resource_group_name=RESOURCE_GROUP, route_table_name=ROUTE_TABLE_NAME, tags=TAGS)


#--------------------------------------------------------------------------
# /RouteTables/delete/Delete route table[delete]
#--------------------------------------------------------------------------
print("Delete route table")
result = mgmt_client.route_tables.delete(resource_group_name=RESOURCE_GROUP, route_table_name=ROUTE_TABLE_NAME)
result = result.result()
