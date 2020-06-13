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
PUBLIC_IP_ADDRESS_NAME = "myPublicIpAddress"
VIRTUAL_NETWORK_NAME = "myVirtualNetwork"
SUBNET_NAME = "GatewaySubnet"
VIRTUAL_NETWORK_GATEWAY_NAME = "myVirtualNetworkGateway"
VIRTUAL_ROUTER_NAME = "myVirtualRouter"
PEERING_NAME = "myPeering"


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
# /PublicIPAddresses/put/Create public IP address defaults[put]
#--------------------------------------------------------------------------
print("Create public IP address defaults")
BODY = {
  "location": AZURE_LOCATION
}
result = mgmt_client.public_ip_addresses.create_or_update(resource_group_name=RESOURCE_GROUP, public_ip_address_name=PUBLIC_IP_ADDRESS_NAME, parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /VirtualNetworks/put/Create virtual network[put]
#--------------------------------------------------------------------------
print("Create virtual network")
BODY = {
  "location": AZURE_LOCATION,
  "address_space": {
    "address_prefixes": [
      "10.0.0.0/16"
    ]
  }
}
result = mgmt_client.virtual_networks.create_or_update(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME, parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /Subnets/put/Create subnet[put]
#--------------------------------------------------------------------------
print("Create subnet")
BODY = {
  "address_prefix": "10.0.0.0/16"
}
result = mgmt_client.subnets.create_or_update(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME, subnet_name=SUBNET_NAME, subnet_parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /VirtualNetworkGateways/put/UpdateVirtualNetworkGateway[put]
#--------------------------------------------------------------------------
print("UpdateVirtualNetworkGateway")
BODY = {
  "location": AZURE_LOCATION,
  "ip_configurations": [
    {
      "name": "gwipconfig1",
      "private_ipallocation_method": "Dynamic",
      "subnet": {
        "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualNetworks/" + VIRTUAL_NETWORK_NAME + "/subnets/" + SUBNET_NAME
      },
      "public_ip_address": {
        "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/publicIPAddresses/" + PUBLIC_IP_ADDRESS_NAME
      }
    }
  ],
  "gateway_type": "Vpn",
  "vpn_type": "RouteBased",
  "enable_bgp": False,
  "active_active": False,
  "enable_dns_forwarding": True,
  "sku": {
    "name": "VpnGw1",
    "tier": "VpnGw1"
  },
  "vpn_client_configuration": {
    "vpn_client_protocols": [
      "OpenVPN"
    ],
    "vpn_client_root_certificates": [],
    "vpn_client_revoked_certificates": [],
    "radius_servers": [
      {
        "radius_server_address": "10.2.0.0",
        "radius_server_score": "20",
        "radius_server_secret": "radiusServerSecret"
      }
    ]
  },
  "bgp_settings": {
    "asn": "65515",
    "bgp_peering_address": "10.0.1.30",
    "peer_weight": "0"
  },
  "custom_routes": {
    "address_prefixes": [
      "101.168.0.6/32"
    ]
  }
}
result = mgmt_client.virtual_network_gateways.create_or_update(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_name=VIRTUAL_NETWORK_GATEWAY_NAME, parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# This feature is not enabled
# /VirtualRouters/put/Create VirtualRouter[put]
#--------------------------------------------------------------------------
print("Create VirtualRouter")
BODY = {
  "tags": {
    "key1": "value1"
  },
  "location": AZURE_LOCATION,
  "hosted_gateway": {
    "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualNetworkGateways/" + VIRTUAL_NETWORK_GATEWAY_NAME
  }
}
# result = mgmt_client.virtual_routers.create_or_update(resource_group_name=RESOURCE_GROUP, virtual_router_name=VIRTUAL_ROUTER_NAME, parameters=BODY)
# result = result.result()


#--------------------------------------------------------------------------
# This feature is not enabled
# /VirtualRouterPeerings/put/Create Virtual Router Peering[put]
#--------------------------------------------------------------------------
print("Create Virtual Router Peering")
BODY = {
  "peer_ip": "192.168.1.5",
  "peer_asn": "20000"
}
# result = mgmt_client.virtual_router_peerings.create_or_update(resource_group_name=RESOURCE_GROUP, virtual_router_name=VIRTUAL_ROUTER_NAME, peering_name=PEERING_NAME, parameters=BODY)
# result = result.result()


#--------------------------------------------------------------------------
# This feature is not enabled
# /VirtualRouterPeerings/get/Get Virtual Router Peering[get]
#--------------------------------------------------------------------------
print("Get Virtual Router Peering")
# result = mgmt_client.virtual_router_peerings.get(resource_group_name=RESOURCE_GROUP, virtual_router_name=VIRTUAL_ROUTER_NAME, peering_name=PEERING_NAME)


#--------------------------------------------------------------------------
# This feature is not enabled
# /VirtualRouterPeerings/get/List all Virtual Router Peerings for a given Virtual Router[get]
#--------------------------------------------------------------------------
print("List all Virtual Router Peerings for a given Virtual Router")
# result = mgmt_client.virtual_router_peerings.list(resource_group_name=RESOURCE_GROUP, virtual_router_name=VIRTUAL_ROUTER_NAME)


#--------------------------------------------------------------------------
# This feature is not enabled
# /VirtualRouterPeerings/delete/Delete VirtualRouterPeering[delete]
#--------------------------------------------------------------------------
print("Delete VirtualRouterPeering")
# result = mgmt_client.virtual_router_peerings.delete(resource_group_name=RESOURCE_GROUP, virtual_router_name=VIRTUAL_ROUTER_NAME, peering_name=PEERING_NAME)
# result = result.result()
