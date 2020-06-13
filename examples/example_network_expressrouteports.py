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
EXPRESS_ROUTE_PORT_NAME = "myExpressRoutePort"


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
# The resource type could not be found in the namespace 'Microsoft.Network' for api version '2020-04-01'
# /ExpressRoutePorts/put/ExpressRoutePortCreate[put]
#--------------------------------------------------------------------------
print("ExpressRoutePortCreate")
BODY = {
  "location": AZURE_LOCATION,
  "peering_location": "peeringLocationName",
  "bandwidth_in_gbps": "100",
  "encapsulation": "QinQ"
}
# result = mgmt_client.express_route_ports.create_or_update(resource_group_name=RESOURCE_GROUP, express_route_port_name=EXPRESS_ROUTE_PORT_NAME, parameters=BODY)
# result = result.result()


#--------------------------------------------------------------------------
# The resource type could not be found in the namespace 'Microsoft.Network' for api version '2020-04-01'
# /ExpressRoutePorts/put/ExpressRoutePortUpdateLink[put]
#--------------------------------------------------------------------------
print("ExpressRoutePortUpdateLink")
BODY = {
  "location": AZURE_LOCATION,
  "peering_location": "peeringLocationName",
  "bandwidth_in_gbps": "100",
  "encapsulation": "QinQ",
  "links": [
    {
      "name": "link1",
      "admin_state": "Enabled"
    }
  ]
}
# result = mgmt_client.express_route_ports.create_or_update(resource_group_name=RESOURCE_GROUP, express_route_port_name=EXPRESS_ROUTE_PORT_NAME, parameters=BODY)
# result = result.result()


#--------------------------------------------------------------------------
# The resource type could not be found in the namespace 'Microsoft.Network' for api version '2020-04-01'
# /ExpressRoutePorts/get/ExpressRoutePortGet[get]
#--------------------------------------------------------------------------
print("ExpressRoutePortGet")
# result = mgmt_client.express_route_ports.get(resource_group_name=RESOURCE_GROUP, express_route_port_name=EXPRESS_ROUTE_PORT_NAME)


#--------------------------------------------------------------------------
# The resource type could not be found in the namespace 'Microsoft.Network' for api version '2020-04-01'
# /ExpressRoutePorts/get/ExpressRoutePortListByResourceGroup[get]
#--------------------------------------------------------------------------
print("ExpressRoutePortListByResourceGroup")
# result = mgmt_client.express_route_ports.list_by_resource_group(resource_group_name=RESOURCE_GROUP)


#--------------------------------------------------------------------------
# The resource type could not be found in the namespace 'Microsoft.Network' for api version '2020-04-01'
# /ExpressRoutePorts/get/ExpressRoutePortList[get]
#--------------------------------------------------------------------------
print("ExpressRoutePortList")
# result = mgmt_client.express_route_ports.list()


#--------------------------------------------------------------------------
# The resource type could not be found in the namespace 'Microsoft.Network' for api version '2020-04-01'
# /ExpressRoutePorts/patch/ExpressRoutePortUpdateTags[patch]
#--------------------------------------------------------------------------
print("ExpressRoutePortUpdateTags")
TAGS = {
  "tag1": "value1",
  "tag2": "value2"
}
# result = mgmt_client.express_route_ports.update_tags(resource_group_name=RESOURCE_GROUP, express_route_port_name=EXPRESS_ROUTE_PORT_NAME, tags=TAGS)


#--------------------------------------------------------------------------
# The resource type could not be found in the namespace 'Microsoft.Network' for api version '2020-04-01'
# /ExpressRoutePorts/delete/ExpressRoutePortDelete[delete]
#--------------------------------------------------------------------------
print("ExpressRoutePortDelete")
# result = mgmt_client.express_route_ports.delete(resource_group_name=RESOURCE_GROUP, express_route_port_name=EXPRESS_ROUTE_PORT_NAME)
# result = result.result()
