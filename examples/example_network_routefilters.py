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
ROUTE_FILTER_NAME = "myRouteFilter"


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
# /RouteFilters/put/RouteFilterCreate[put]
#--------------------------------------------------------------------------
print("RouteFilterCreate")
BODY = {
  "location": AZURE_LOCATION,
  "tags": {
    "key1": "value1"
  },
  "rules": [
    {
      "name": "ruleName",
      "access": "Allow",
      "route_filter_rule_type": "Community",
      "communities": [
        "12076:5030",
        "12076:5040"
      ]
    }
  ]
}
result = mgmt_client.route_filters.create_or_update(resource_group_name=RESOURCE_GROUP, route_filter_name=ROUTE_FILTER_NAME, route_filter_parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /RouteFilters/get/RouteFilterGet[get]
#--------------------------------------------------------------------------
print("RouteFilterGet")
result = mgmt_client.route_filters.get(resource_group_name=RESOURCE_GROUP, route_filter_name=ROUTE_FILTER_NAME)


#--------------------------------------------------------------------------
# /RouteFilters/get/RouteFilterListByResourceGroup[get]
#--------------------------------------------------------------------------
print("RouteFilterListByResourceGroup")
result = mgmt_client.route_filters.list_by_resource_group(resource_group_name=RESOURCE_GROUP)


#--------------------------------------------------------------------------
# /RouteFilters/get/RouteFilterList[get]
#--------------------------------------------------------------------------
print("RouteFilterList")
result = mgmt_client.route_filters.list()


#--------------------------------------------------------------------------
# /RouteFilters/patch/Update route filter tags[patch]
#--------------------------------------------------------------------------
print("Update route filter tags")
TAGS = {
  "key1": "value1"
}
result = mgmt_client.route_filters.update_tags(resource_group_name=RESOURCE_GROUP, route_filter_name=ROUTE_FILTER_NAME, tags=TAGS)


#--------------------------------------------------------------------------
# /RouteFilters/delete/RouteFilterDelete[delete]
#--------------------------------------------------------------------------
print("RouteFilterDelete")
result = mgmt_client.route_filters.delete(resource_group_name=RESOURCE_GROUP, route_filter_name=ROUTE_FILTER_NAME)
result = result.result()
