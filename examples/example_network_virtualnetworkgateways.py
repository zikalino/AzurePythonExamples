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
VIRTUAL_NETWORK_GATEWAY_CONNECTION_NAME = "myVirtualNetworkGatewayConnection"


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
#result = mgmt_client.public_ip_addresses.create_or_update(resource_group_name=RESOURCE_GROUP, public_ip_address_name=PUBLIC_IP_ADDRESS_NAME, parameters=BODY)
#result = result.result()


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
#result = mgmt_client.virtual_networks.create_or_update(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME, parameters=BODY)
#result = result.result()


#--------------------------------------------------------------------------
# /Subnets/put/Create subnet[put]
#--------------------------------------------------------------------------
print("Create subnet")
BODY = {
  "address_prefix": "10.0.0.0/16"
}
#result = mgmt_client.subnets.create_or_update(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME, subnet_name=SUBNET_NAME, subnet_parameters=BODY)
#result = result.result()


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
  "enable_dns_forwarding": False,
  "sku": {
    "name": "VpnGw1",
    "tier": "VpnGw1"
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
#result = mgmt_client.virtual_network_gateways.create_or_update(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_name=VIRTUAL_NETWORK_GATEWAY_NAME, parameters=BODY)
#result = result.result()


#--------------------------------------------------------------------------
# /VirtualNetworkGateways/get/VirtualNetworkGatewaysListConnections[get]
#--------------------------------------------------------------------------
print("VirtualNetworkGatewaysListConnections")
result = mgmt_client.virtual_network_gateways.list_connections(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_name=VIRTUAL_NETWORK_GATEWAY_NAME)


#--------------------------------------------------------------------------
# /VirtualNetworkGateways/get/GetVirtualNetworkGateway[get]
#--------------------------------------------------------------------------
print("GetVirtualNetworkGateway")
result = mgmt_client.virtual_network_gateways.get(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_name=VIRTUAL_NETWORK_GATEWAY_NAME)


#--------------------------------------------------------------------------
# /VirtualNetworkGateways/get/ListVirtualNetworkGatewaysinResourceGroup[get]
#--------------------------------------------------------------------------
print("ListVirtualNetworkGatewaysinResourceGroup")
result = mgmt_client.virtual_network_gateways.list(resource_group_name=RESOURCE_GROUP)


#--------------------------------------------------------------------------
# /VirtualNetworkGateways/post/Disconnect VpnConnections from Virtual Network Gateway[post]
#--------------------------------------------------------------------------
print("Disconnect VpnConnections from Virtual Network Gateway")
VPN_CONNECTION_IDS = [
  "vpnconnId1",
  "vpnconnId2"
]
#result = mgmt_client.virtual_network_gateways.disconnect_virtual_network_gateway_vpn_connections(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_name=VIRTUAL_NETWORK_GATEWAY_NAME, vpn_connection_ids=VPN_CONNECTION_IDS)
#result = result.result()


#--------------------------------------------------------------------------
# /VirtualNetworkGateways/post/GetVPNDeviceConfigurationScript[post]
#--------------------------------------------------------------------------
print("GetVPNDeviceConfigurationScript")
BODY = {
  "vendor": "Cisco",
  "device_family": "ISR",
  "firmware_version": "IOS 15.1 (Preview)"
}
#result = mgmt_client.virtual_network_gateways.vpn_device_configuration_script(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_connection_name=VIRTUAL_NETWORK_GATEWAY_CONNECTION_NAME, parameters=BODY)


#--------------------------------------------------------------------------
# /VirtualNetworkGateways/post/GetVirtualNetworkGatewayVpnclientConnectionHealth[post]
#--------------------------------------------------------------------------
print("GetVirtualNetworkGatewayVpnclientConnectionHealth")
#result = mgmt_client.virtual_network_gateways.get_vpnclient_connection_health(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_name=VIRTUAL_NETWORK_GATEWAY_NAME)
#result = result.result()


#--------------------------------------------------------------------------
# /VirtualNetworkGateways/post/Set VirtualNetworkGateway VpnClientIpsecParameters[post]
#--------------------------------------------------------------------------
print("Set VirtualNetworkGateway VpnClientIpsecParameters")
BODY = {
  "sa_life_time_seconds": "86473",
  "sa_data_size_kilobytes": "429497",
  "ipsec_encryption": "AES256",
  "ipsec_integrity": "SHA256",
  "ike_encryption": "AES256",
  "ike_integrity": "SHA384",
  "dh_group": "DHGroup2",
  "pfs_group": "PFS2"
}
#result = mgmt_client.virtual_network_gateways.set_vpnclient_ipsec_parameters(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_name=VIRTUAL_NETWORK_GATEWAY_NAME, vpnclient_ipsec_params=BODY)
#result = result.result()


#--------------------------------------------------------------------------
# /VirtualNetworkGateways/post/Get VirtualNetworkGateway VpnClientIpsecParameters[post]
#--------------------------------------------------------------------------
print("Get VirtualNetworkGateway VpnClientIpsecParameters")
#result = mgmt_client.virtual_network_gateways.get_vpnclient_ipsec_parameters(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_name=VIRTUAL_NETWORK_GATEWAY_NAME)
#result = result.result()


#--------------------------------------------------------------------------
# /VirtualNetworkGateways/post/GenerateVPNClientPackage[post]
#--------------------------------------------------------------------------
print("GenerateVPNClientPackage")
BODY = {}
#result = mgmt_client.virtual_network_gateways.generatevpnclientpackage(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_name=VIRTUAL_NETWORK_GATEWAY_NAME, parameters=BODY)
#result = result.result()


#--------------------------------------------------------------------------
# /VirtualNetworkGateways/post/GetVirtualNetworkGatewayVPNProfilePackageURL[post]
#--------------------------------------------------------------------------
print("GetVirtualNetworkGatewayVPNProfilePackageURL")
#result = mgmt_client.virtual_network_gateways.get_vpn_profile_package_url(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_name=VIRTUAL_NETWORK_GATEWAY_NAME)
#result = result.result()


#--------------------------------------------------------------------------
# /VirtualNetworkGateways/post/ResetVpnClientSharedKey[post]
#--------------------------------------------------------------------------
print("ResetVpnClientSharedKey")
#result = mgmt_client.virtual_network_gateways.reset_vpn_client_shared_key(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_name=VIRTUAL_NETWORK_GATEWAY_NAME)
#result = result.result()


#--------------------------------------------------------------------------
# /VirtualNetworkGateways/post/ListVirtualNetworkGatewaySupportedVPNDevices[post]
#--------------------------------------------------------------------------
print("ListVirtualNetworkGatewaySupportedVPNDevices")
result = mgmt_client.virtual_network_gateways.supported_vpn_devices(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_name=VIRTUAL_NETWORK_GATEWAY_NAME)


#--------------------------------------------------------------------------
# /VirtualNetworkGateways/post/GetVirtualNetworkGatewayAdvertisedRoutes[post]
#--------------------------------------------------------------------------
print("GetVirtualNetworkGatewayAdvertisedRoutes")
#result = mgmt_client.virtual_network_gateways.get_advertised_routes(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_name=VIRTUAL_NETWORK_GATEWAY_NAME, peer="test")
#result = result.result()


#--------------------------------------------------------------------------
# /VirtualNetworkGateways/post/Start packet capture on virtual network gateway without filter[post]
#--------------------------------------------------------------------------
print("Start packet capture on virtual network gateway without filter")
#result = mgmt_client.virtual_network_gateways.start_packet_capture(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_name=VIRTUAL_NETWORK_GATEWAY_NAME)
#result = result.result()


#--------------------------------------------------------------------------
# /VirtualNetworkGateways/post/Start packet capture on virtual network gateway with filter[post]
#--------------------------------------------------------------------------
print("Start packet capture on virtual network gateway with filter")
#result = mgmt_client.virtual_network_gateways.start_packet_capture(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_name=VIRTUAL_NETWORK_GATEWAY_NAME, filter_data="{'TracingFlags': 11,'MaxPacketBufferSize': 120,'MaxFileSize': 200,'Filters': [{'SourceSubnets': ['20.1.1.0/24'],'DestinationSubnets': ['10.1.1.0/24'],'SourcePort': [500],'DestinationPort': [4500],'Protocol': 6,'TcpFlags': 16,'CaptureSingleDirectionTrafficOnly': true}]}")
#result = result.result()


#--------------------------------------------------------------------------
# /VirtualNetworkGateways/post/GenerateVirtualNetworkGatewayVPNProfile[post]
#--------------------------------------------------------------------------
print("GenerateVirtualNetworkGatewayVPNProfile")
BODY = {}
#result = mgmt_client.virtual_network_gateways.generate_vpn_profile(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_name=VIRTUAL_NETWORK_GATEWAY_NAME, parameters=BODY)
#result = result.result()


#--------------------------------------------------------------------------
# /VirtualNetworkGateways/post/Stop packet capture on virtual network gateway[post]
#--------------------------------------------------------------------------
print("Stop packet capture on virtual network gateway")
#result = mgmt_client.virtual_network_gateways.stop_packet_capture(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_name=VIRTUAL_NETWORK_GATEWAY_NAME, sas_url="https://teststorage.blob.core.windows.net/?sv=2018-03-28&ss=bfqt&srt=sco&sp=rwdlacup&se=2019-09-13T07:44:05Z&st=2019-09-06T23:44:05Z&spr=https&sig=V1h9D1riltvZMI69d6ihENnFo%2FrCvTqGgjO2lf%2FVBhE%3D")
#result = result.result()


#--------------------------------------------------------------------------
# /VirtualNetworkGateways/post/GetVirtualNetworkGatewayLearnedRoutes[post]
#--------------------------------------------------------------------------
print("GetVirtualNetworkGatewayLearnedRoutes")
result = mgmt_client.virtual_network_gateways.get_learned_routes(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_name=VIRTUAL_NETWORK_GATEWAY_NAME)
result = result.result()


#--------------------------------------------------------------------------
# /VirtualNetworkGateways/post/GetVirtualNetworkGatewayBGPPeerStatus[post]
#--------------------------------------------------------------------------
print("GetVirtualNetworkGatewayBGPPeerStatus")
result = mgmt_client.virtual_network_gateways.get_bgp_peer_status(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_name=VIRTUAL_NETWORK_GATEWAY_NAME)
result = result.result()


#--------------------------------------------------------------------------
# /VirtualNetworkGateways/post/ResetVirtualNetworkGateway[post]
#--------------------------------------------------------------------------
print("ResetVirtualNetworkGateway")
result = mgmt_client.virtual_network_gateways.reset(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_name=VIRTUAL_NETWORK_GATEWAY_NAME)
result = result.result()


#--------------------------------------------------------------------------
# /VirtualNetworkGateways/patch/UpdateVirtualNetworkGatewayTags[patch]
#--------------------------------------------------------------------------
print("UpdateVirtualNetworkGatewayTags")
TAGS = {
  "tag1": "value1",
  "tag2": "value2"
}
#result = mgmt_client.virtual_network_gateways.update_tags(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_name=VIRTUAL_NETWORK_GATEWAY_NAME, tags=TAGS)
#result = result.result()


#--------------------------------------------------------------------------
# /VirtualNetworkGateways/delete/DeleteVirtualNetworkGateway[delete]
#--------------------------------------------------------------------------
print("DeleteVirtualNetworkGateway")
result = mgmt_client.virtual_network_gateways.delete(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_name=VIRTUAL_NETWORK_GATEWAY_NAME)
result = result.result()
