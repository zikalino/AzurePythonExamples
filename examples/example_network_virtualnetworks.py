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
VIRTUAL_NETWORK_NAME = "myVirtualNetwork"
SERVICE_ENDPOINT_POLICY_NAME = "myServiceEndpointPolicy"


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
# /VirtualNetworks/put/Create virtual network with service endpoints and service endpoint policy[put]
#--------------------------------------------------------------------------
print("Create virtual network with service endpoints and service endpoint policy")
BODY = {
  "properties": {
    "address_space": {
      "address_prefixes": [
        "10.0.0.0/16"
      ]
    },
    "subnets": [
      {
        "name": "test-1",
        "properties": {
          "address_prefix": "10.0.0.0/16",
          "service_endpoints": [
            {
              "service": "Microsoft.Storage"
            }
          ],
          "service_endpoint_policies": [
            {
              "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/serviceEndpointPolicies/" + SERVICE_ENDPOINT_POLICY_NAME
            }
          ]
        }
      }
    ]
  },
  "location": AZURE_LOCATION
}
#result = mgmt_client.virtual_networks.create_or_update(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME, parameters=BODY)
#result = result.result()


#--------------------------------------------------------------------------
# /VirtualNetworks/put/Create virtual network with subnet containing address prefixes[put]
#--------------------------------------------------------------------------
print("Create virtual network with subnet containing address prefixes")
BODY = {
  "address_space": {
    "address_prefixes": [
      "10.0.0.0/16"
    ]
  },
  "subnets": [
    {
      "name": "test-2",
      "address_prefixes": [
        "10.0.0.0/28",
        "10.0.1.0/28"
      ]
    }
  ],
  "location": AZURE_LOCATION
}
# result = mgmt_client.virtual_networks.create_or_update(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME, parameters=BODY)
# result = result.result()


#--------------------------------------------------------------------------
# /VirtualNetworks/put/Create virtual network with Bgp Communities[put]
#--------------------------------------------------------------------------
print("Create virtual network with Bgp Communities")
BODY = {
  "address_space": {
    "address_prefixes": [
      "10.0.0.0/16"
    ]
  },
  "subnets": [
    {
      "name": "test-1",
      "address_prefix": "10.0.0.0/24"
    }
  ],
  "bgp_communities": {
    "virtual_network_community": "12076:49999"
  },
  "location": AZURE_LOCATION
}
result = mgmt_client.virtual_networks.create_or_update(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME, parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /VirtualNetworks/put/Create virtual network[put]
#--------------------------------------------------------------------------
print("Create virtual network")
BODY = {
  "address_space": {
    "address_prefixes": [
      "10.0.0.0/16"
    ]
  },
  "location": AZURE_LOCATION
}
result = mgmt_client.virtual_networks.create_or_update(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME, parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /VirtualNetworks/put/Create virtual network with service endpoints[put]
#--------------------------------------------------------------------------
print("Create virtual network with service endpoints")
BODY = {
  "address_space": {
    "address_prefixes": [
      "10.0.0.0/16"
    ]
  },
  "subnets": [
    {
      "name": "test-1",
      "address_prefix": "10.0.0.0/16",
      "service_endpoints": [
        {
          "service": "Microsoft.Storage"
        }
      ]
    }
  ],
  "location": AZURE_LOCATION
}
result = mgmt_client.virtual_networks.create_or_update(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME, parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /VirtualNetworks/put/Create virtual network with subnet[put]
#--------------------------------------------------------------------------
print("Create virtual network with subnet")
BODY = {
  "address_space": {
    "address_prefixes": [
      "10.0.0.0/16"
    ]
  },
  "subnets": [
    {
      "name": "test-1",
      "address_prefix": "10.0.0.0/24"
    }
  ],
  "location": AZURE_LOCATION
}
result = mgmt_client.virtual_networks.create_or_update(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME, parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /VirtualNetworks/put/Create virtual network with delegated subnets[put]
#--------------------------------------------------------------------------
print("Create virtual network with delegated subnets")
BODY = {
  "address_space": {
    "address_prefixes": [
      "10.0.0.0/16"
    ]
  },
  "subnets": [
    {
      "name": "test-1",
      "address_prefix": "10.0.0.0/24",
      "delegations": [
        {
          "name": "myDelegation",
          "properties": {
            "service_name": "Microsoft.Sql/managedInstances"
          }
        }
      ]
    }
  ],
  "location": AZURE_LOCATION
}
# result = mgmt_client.virtual_networks.create_or_update(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME, parameters=BODY)
# result = result.result()


#--------------------------------------------------------------------------
# /VirtualNetworks/get/Check IP address availability[get]
#--------------------------------------------------------------------------
print("Check IP address availability")
result = mgmt_client.virtual_networks.check_ip_address_availability(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME, ip_address="10.0.0.4")


#--------------------------------------------------------------------------
# /VirtualNetworks/get/VnetGetUsage[get]
#--------------------------------------------------------------------------
print("VnetGetUsage")
result = mgmt_client.virtual_networks.list_usage(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME)


#--------------------------------------------------------------------------
# /VirtualNetworks/get/Get virtual network[get]
#--------------------------------------------------------------------------
print("Get virtual network")
result = mgmt_client.virtual_networks.get(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME)


#--------------------------------------------------------------------------
# /VirtualNetworks/get/Get virtual network with service association links[get]
#--------------------------------------------------------------------------
print("Get virtual network with service association links")
result = mgmt_client.virtual_networks.get(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME)


#--------------------------------------------------------------------------
# /VirtualNetworks/get/Get virtual network with a delegated subnet[get]
#--------------------------------------------------------------------------
print("Get virtual network with a delegated subnet")
result = mgmt_client.virtual_networks.get(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME)


#--------------------------------------------------------------------------
# /VirtualNetworks/get/List virtual networks in resource group[get]
#--------------------------------------------------------------------------
print("List virtual networks in resource group")
result = mgmt_client.virtual_networks.list(resource_group_name=RESOURCE_GROUP)


#--------------------------------------------------------------------------
# /VirtualNetworks/get/List all virtual networks[get]
#--------------------------------------------------------------------------
print("List all virtual networks")
result = mgmt_client.virtual_networks.list_all()


#--------------------------------------------------------------------------
# /VirtualNetworks/patch/Update virtual network tags[patch]
#--------------------------------------------------------------------------
print("Update virtual network tags")
TAGS = {
  "tag1": "value1",
  "tag2": "value2"
}
result = mgmt_client.virtual_networks.update_tags(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME, tags=TAGS)


#--------------------------------------------------------------------------
# /VirtualNetworks/delete/Delete virtual network[delete]
#--------------------------------------------------------------------------
print("Delete virtual network")
result = mgmt_client.virtual_networks.delete(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME)
result = result.result()
