#-------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#--------------------------------------------------------------------------

import os
from azure.mgmt.peering import PeeringManagementClient
from azure.mgmt.resource import ResourceManagementClient
# from azure.common.credentials import ServicePrincipalCredentials
from azure.common.credentials import get_azure_cli_credentials
cred, sub, tenant = get_azure_cli_credentials(with_tenant=True)

AZURE_LOCATION = 'eastus'
RESOURCE_GROUP = "myResourceGroup"
# credentials from environment
#SUBSCRIPTION_ID = os.environ['AZURE_SUBSCRIPTION_ID']
SUBSCRIPTION_ID='xxx'
#TENANT_ID = os.environ['AZURE_TENANT']
#CLIENT_ID = os.environ['AZURE_CLIENT_ID']
#CLIENT_SECRET = os.environ['AZURE_SECRET']
PEER_ASN_NAME = "myPeerAsn"
PEERING_NAME = "myPeering" + "B"
REGISTERED_ASN_NAME = "myRegisteredAsn"
REGISTERED_PREFIX_NAME = "myRegisteredPrefix"
PEERING_SERVICE_NAME = "myPeeringService"
PREFIX_NAME = "myPrefix"
# management client
#credentials = ServicePrincipalCredentials(
#    client_id=CLIENT_ID,
#    secret=CLIENT_SECRET,
#    tenant=TENANT_ID
#)
mgmt_client = PeeringManagementClient(credentials=cred, subscription_id=sub, base_url='https://api-dogfood.resources.windows-int.net/')
resource_client = ResourceManagementClient(credentials=cred, subscription_id=sub, base_url='https://api-dogfood.resources.windows-int.net/')
# CREATE RESOURCE GROUP
print("Creating Resource Group")
resource_client.resource_groups.create_or_update(resource_group_name=RESOURCE_GROUP, parameters={ 'location': AZURE_LOCATION })


# /PeerAsns/put/Create a peer ASN[put]
print("Create a peer ASN")
BODY = {
  "peer_asn": "65001",
  "peer_contact_detail": [
    {
      "role": "Noc",
      "email": "noc@contoso.com",
      "phone": "+1 (234) 567-8999"
    },
    {
      "role": "Policy",
      "email": "abc@contoso.com",
      "phone": "+1 (234) 567-8900"
    },
    {
      "role": "Technical",
      "email": "xyz@contoso.com",
      "phone": "+1 (234) 567-8900"
    }
  ],
  "peer_name": "Contoso",
  "validation_state": "Approved"
}
result = mgmt_client.peer_asns.create_or_update(peer_asn_name=PEER_ASN_NAME, peer_asn=BODY)

print("Update a peer ASN")
BODY = {
  "validation_state": "Approved"
}
#result = mgmt_client.peer_asns.update(peer_asn_name=PEER_ASN_NAME, peer_asn=BODY)


# /PeerAsns/get/Get a peer ASN[get]
print("Get a peer ASN")
result = mgmt_client.peer_asns.get(peer_asn_name=PEER_ASN_NAME)

print(result)

# /Peerings/put/Create an exchange peering[put]
print("Create an exchange peering")
BODY = {
  "sku": {
    "name": "Basic_Exchange_Free"
  },
  "kind": "Exchange",
  "location": "centralus",
  "exchange": {
    "connections": [
      {
        "peering_db_facility_id": "99999",
        "bgp_session": {
          "peer_session_ipv4_address": "80.249.231.0",
          #"peer_session_ipv6_address": "fd00::1",
          "max_prefixes_advertised_v4": "1000",
          #"max_prefixes_advertised_v6": "100",
          "md5authentication_key": "test-md5-auth-key"
        },
        "connection_identifier": "CE495334-0E94-4E51-8164-8116D6CD284D"
      },
      {
        "peering_db_facility_id": "99999",
        "bgp_session": {
          "peer_session_ipv4_address": "80.249.232.0",
          #"peer_session_ipv6_address": "fd00::2",
          "max_prefixes_advertised_v4": "1000",
          #"max_prefixes_advertised_v6": "100",
          "md5authentication_key": "test-md5-auth-key"
        },
        "connection_identifier": "CDD8E673-CB07-47E6-84DE-3739F778762B"
      }
    ],
    "peer_asn": {
      "id": "/subscriptions/" + SUBSCRIPTION_ID + "/providers/Microsoft.Peering/peerAsns/" + PEER_ASN_NAME
    }
  },
  "peering_location": "Seattle"
}
result = mgmt_client.peerings.create_or_update(resource_group_name=RESOURCE_GROUP, peering_name=PEERING_NAME, peering=BODY)

# /Peerings/put/Create a peering with exchange route server[put]
print("Create a peering with exchange route server")
BODY = {
  "sku": {
    "name": "Premium_Direct_Free"
  },
  "kind": "Direct",
  "location": AZURE_LOCATION,
  "direct": {
    "connections": [
      {
        "bandwidth_in_mbps": "10000",
        "session_address_provider": "Peer",
        "use_for_peering_service": True,
        "peering_db_facility_id": "99999",
        "bgp_session": {
          "session_prefix_v4": "80.249.231.0/24",
          "microsoft_session_ipv4_address": "80.249.231.20",
          "peer_session_ipv4_address": "80.249.231.0",
          "max_prefixes_advertised_v4": "100",
          "max_prefixes_advertised_v6": "0"
        },
        "connection_identifier": "5F4CB5C7-6B43-4444-9338-9ABC72606C16"
      }
    ],
    "peer_asn": {
      "id": "/subscriptions/" + SUBSCRIPTION_ID + "/providers/Microsoft.Peering/peerAsns/" + PEER_ASN_NAME
    },
    "direct_peering_type": "IxRs"
  },
  "peering_location": "Seattle"
}
# result = mgmt_client.peerings.create_or_update(resource_group_name=RESOURCE_GROUP, peering_name=PEERING_NAME, peering=BODY)

# /Peerings/put/Create a direct peering[put]
print("Create a direct peering")
BODY = {
  "sku": {
    "name": "Basic_Direct_Free"
  },
  "kind": "Direct",
  "location": AZURE_LOCATION,
  "direct": {
    "connections": [
      {
        "bandwidth_in_mbps": "10000",
        "session_address_provider": "Peer",
        "use_for_peering_service": False,
        "peering_dbfacility_id": "99999",
        "bgp_session": {
          "session_prefix_v4": "192.168.0.0/31",
          "session_prefix_v6": "fd00::0/127",
          "max_prefixes_advertised_v4": "1000",
          "max_prefixes_advertised_v6": "100",
          "md5authentication_key": "test-md5-auth-key"
        },
        "connection_identifier": "5F4CB5C7-6B43-4444-9338-9ABC72606C16"
      },
      {
        "bandwidth_in_mbps": "10000",
        "session_address_provider": "Microsoft",
        "use_for_peering_service": True,
        "peering_dbfacility_id": "99999",
        "connection_identifier": "8AB00818-D533-4504-A25A-03A17F61201C"
      }
    ],
    "peer_asn": {
      "id": "/subscriptions/" + SUBSCRIPTION_ID + "/providers/Microsoft.Peering/peerAsns/" + PEER_ASN_NAME
    },
    "direct_peering_type": "Edge"
  },
  "peering_location": "peeringLocation0"
}
# result = mgmt_client.peerings.create_or_update(resource_group_name=RESOURCE_GROUP, peering_name=PEERING_NAME, peering=BODY)


# /Peerings/get/Get a peering[get]
print("Get a peering")
result = mgmt_client.peerings.get(resource_group_name=RESOURCE_GROUP, peering_name=PEERING_NAME)
print(result)

# /RegisteredPrefixes/put/Create or update a registered prefix for the peering[put]
print("Create or update a registered prefix for the peering")
result = mgmt_client.registered_prefixes.create_or_update(resource_group_name=RESOURCE_GROUP, peering_name=PEERING_NAME, registered_prefix_name=REGISTERED_PREFIX_NAME, prefix="80.249.231.0/24")
print(result)


# /PeeringServices/put/Create a  peering service[put]
print("Create a  peering service")
BODY = {
  "location": AZURE_LOCATION,
  "peering_service_location": "state1",
  "peering_service_provider": "serviceProvider1"
}
result = mgmt_client.peering_services.create_or_update(resource_group_name=RESOURCE_GROUP, peering_service_name=PEERING_SERVICE_NAME, peering_service=BODY)

# /RegisteredAsns/put/Create or update a registered ASN for the peering[put]
print("Create or update a registered ASN for the peering")
result = mgmt_client.registered_asns.create_or_update(resource_group_name=RESOURCE_GROUP, peering_name=PEERING_NAME, registered_asn_name=REGISTERED_ASN_NAME, asn="65000")

# /Prefixes/put/Create or update a prefix for the peering service[put]
print("Create or update a prefix for the peering service")
result = mgmt_client.prefixes.create_or_update(resource_group_name=RESOURCE_GROUP, peering_service_name=PEERING_SERVICE_NAME, prefix_name=PREFIX_NAME, prefix="80.249.231.0/24", peering_service_prefix_key="00000000-0000-0000-0000-000000000000")

# /RegisteredPrefixes/get/Get a registered prefix associated with the peering[get]
print("Get a registered prefix associated with the peering")
result = mgmt_client.registered_prefixes.get(resource_group_name=RESOURCE_GROUP, peering_name=PEERING_NAME, registered_prefix_name=REGISTERED_PREFIX_NAME)

# /Prefixes/get/Get a prefix associated with the peering service[get]
print("Get a prefix associated with the peering service")
result = mgmt_client.prefixes.get(resource_group_name=RESOURCE_GROUP, peering_service_name=PEERING_SERVICE_NAME, prefix_name=PREFIX_NAME)

# /RegisteredAsns/get/Get a registered ASN associated with the peering[get]
print("Get a registered ASN associated with the peering")
result = mgmt_client.registered_asns.get(resource_group_name=RESOURCE_GROUP, peering_name=PEERING_NAME, registered_asn_name=REGISTERED_ASN_NAME)

# /Prefixes/get/List all the prefixes associated with the peering service[get]
print("List all the prefixes associated with the peering service")
result = mgmt_client.prefixes.list_by_peering_service(resource_group_name=RESOURCE_GROUP, peering_service_name=PEERING_SERVICE_NAME)

# /RegisteredPrefixes/get/List all the registered prefixes associated with the peering[get]
print("List all the registered prefixes associated with the peering")
result = mgmt_client.registered_prefixes.list_by_peering(resource_group_name=RESOURCE_GROUP, peering_name=PEERING_NAME)

# /PeeringServices/get/Get a peering service[get]
print("Get a peering service")
result = mgmt_client.peering_services.get(resource_group_name=RESOURCE_GROUP, peering_service_name=PEERING_SERVICE_NAME)

# /RegisteredAsns/get/List all the registered ASNs associated with the peering[get]
print("List all the registered ASNs associated with the peering")
result = mgmt_client.registered_asns.list_by_peering(resource_group_name=RESOURCE_GROUP, peering_name=PEERING_NAME)

# /PeeringServices/get/List peering services in a resource group[get]
print("List peering services in a resource group")
result = mgmt_client.peering_services.list_by_resource_group(resource_group_name=RESOURCE_GROUP)

# /Peerings/get/List peerings in a resource group[get]
print("List peerings in a resource group")
result = mgmt_client.peerings.list_by_resource_group(resource_group_name=RESOURCE_GROUP)

# /PeeringServiceCountries/get/List peering service countries[get]
print("List peering service countries")
result = mgmt_client.peering_service_countries.list()

# /PeeringServiceLocations/get/List peering service locations[get]
print("List peering service locations")
result = mgmt_client.peering_service_locations.list()

# /PeeringServiceProviders/get/List peering service providers[get]
print("List peering service providers")
result = mgmt_client.peering_service_providers.list()

# /PeeringLocations/get/List exchange peering locations[get]
print("List exchange peering locations")
result = mgmt_client.peering_locations.list(kind="Exchange")

# /PeeringLocations/get/List direct peering locations[get]
print("List direct peering locations")
result = mgmt_client.peering_locations.list(kind="Direct")

# /PeeringServices/get/List peering services in a subscription[get]
print("List peering services in a subscription")
result = mgmt_client.peering_services.list_by_subscription()

# /LegacyPeerings/get/List legacy peerings[get]
print("List legacy peerings")
result = mgmt_client.legacy_peerings.list(peering_location="peeringLocation0", kind="Exchange")

# /PeerAsns/get/List peer ASNs in a subscription[get]
print("List peer ASNs in a subscription")
result = mgmt_client.peer_asns.list_by_subscription()

# /Peerings/get/List peerings in a subscription[get]
print("List peerings in a subscription")
result = mgmt_client.peerings.list_by_subscription()

# /Operations/get/List peering operations[get]
print("List peering operations")
result = mgmt_client.operations.list()

# /PeeringServices/patch/Update peering service tags[patch]
print("Update peering service tags")
TAGS = {
  "tag0": "value0",
  "tag1": "value1"
}
result = mgmt_client.peering_services.update(resource_group_name=RESOURCE_GROUP, peering_service_name=PEERING_SERVICE_NAME, tags=TAGS)

# /Peerings/patch/Update peering tags[patch]
print("Update peering tags")
TAGS = {
  "tag0": "value0",
  "tag1": "value1"
}
result = mgmt_client.peerings.update(resource_group_name=RESOURCE_GROUP, peering_name=PEERING_NAME, tags=TAGS)

# //post/Check if peering service provider is available in customer location[post]
print("Check if peering service provider is available in customer location")
result = mgmt_client.check_service_provider_availability(peering_service_location="peeringServiceLocation1", peering_service_provider="peeringServiceProvider1")

# /RegisteredPrefixes/delete/Deletes a registered prefix associated with the peering[delete]
print("Deletes a registered prefix associated with the peering")
result = mgmt_client.registered_prefixes.delete(resource_group_name=RESOURCE_GROUP, peering_name=PEERING_NAME, registered_prefix_name=REGISTERED_PREFIX_NAME)

# /Prefixes/delete/Delete a prefix associated with the peering service[delete]
print("Delete a prefix associated with the peering service")
result = mgmt_client.prefixes.delete(resource_group_name=RESOURCE_GROUP, peering_service_name=PEERING_SERVICE_NAME, prefix_name=PREFIX_NAME)

# /RegisteredAsns/delete/Deletes a registered ASN associated with the peering[delete]
print("Deletes a registered ASN associated with the peering")
result = mgmt_client.registered_asns.delete(resource_group_name=RESOURCE_GROUP, peering_name=PEERING_NAME, registered_asn_name=REGISTERED_ASN_NAME)

# /PeeringServices/delete/Delete a peering service[delete]
print("Delete a peering service")
result = mgmt_client.peering_services.delete(resource_group_name=RESOURCE_GROUP, peering_service_name=PEERING_SERVICE_NAME)

# /Peerings/delete/Delete a peering[delete]
print("Delete a peering")
result = mgmt_client.peerings.delete(resource_group_name=RESOURCE_GROUP, peering_name=PEERING_NAME)

# /PeerAsns/delete/Delete a peer ASN[delete]
print("Delete a peer ASN")
#result = mgmt_client.peer_asns.delete(peer_asn_name=PEER_ASN_NAME)