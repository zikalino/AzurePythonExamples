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
VPN_SITE_NAME = "myVpnSite"
VIRTUAL_WAN_NAME = "myVirtualWan"


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
# /VirtualWans/put/VirtualWANCreate[put]
#--------------------------------------------------------------------------
print("VirtualWANCreate")
BODY = {
  "location": AZURE_LOCATION,
  "tags": {
    "key1": "value1"
  },
  "disable_vpn_encryption": False,
  "type": "Basic"
}
result = mgmt_client.virtual_wans.create_or_update(resource_group_name=RESOURCE_GROUP, virtual_wan_name=VIRTUAL_WAN_NAME, wan_parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /VpnSites/put/VpnSiteCreate[put]
#--------------------------------------------------------------------------
print("VpnSiteCreate")
BODY = {
  "tags": {
    "key1": "value1"
  },
  "location": AZURE_LOCATION,
  "virtual_wan": {
    "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualWANs/" + VIRTUAL_WAN_NAME
  },
  "address_space": {
    "address_prefixes": [
      "10.0.0.0/16"
    ]
  },
  "is_security_site": False,
  "vpn_site_links": [
    {
      "name": "vpnSiteLink1",
      "ip_address": "50.50.50.56",
      "fqdn": "link1.vpnsite1.contoso.com",
      "link_properties": {
        "link_provider_name": "vendor1",
        "link_speed_in_mbps": "0"
      },
      "bgp_properties": {
        "bgp_peering_address": "192.168.0.0",
        "asn": "1234"
      }
    }
  ]
}
result = mgmt_client.vpn_sites.create_or_update(resource_group_name=RESOURCE_GROUP, vpn_site_name=VPN_SITE_NAME, vpn_site_parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /VpnSites/get/VpnSiteGet[get]
#--------------------------------------------------------------------------
print("VpnSiteGet")
result = mgmt_client.vpn_sites.get(resource_group_name=RESOURCE_GROUP, vpn_site_name=VPN_SITE_NAME)


#--------------------------------------------------------------------------
# /VpnSites/get/VpnSiteListByResourceGroup[get]
#--------------------------------------------------------------------------
print("VpnSiteListByResourceGroup")
result = mgmt_client.vpn_sites.list_by_resource_group(resource_group_name=RESOURCE_GROUP)


#--------------------------------------------------------------------------
# /VpnSites/get/VpnSiteList[get]
#--------------------------------------------------------------------------
print("VpnSiteList")
result = mgmt_client.vpn_sites.list()


#--------------------------------------------------------------------------
# /VpnSites/patch/VpnSiteUpdate[patch]
#--------------------------------------------------------------------------
print("VpnSiteUpdate")
TAGS = {
  "key1": "value1",
  "key2": "value2"
}
result = mgmt_client.vpn_sites.update_tags(resource_group_name=RESOURCE_GROUP, vpn_site_name=VPN_SITE_NAME, tags=TAGS)


#--------------------------------------------------------------------------
# /VpnSites/delete/VpnSiteDelete[delete]
#--------------------------------------------------------------------------
print("VpnSiteDelete")
result = mgmt_client.vpn_sites.delete(resource_group_name=RESOURCE_GROUP, vpn_site_name=VPN_SITE_NAME)
result = result.result()
