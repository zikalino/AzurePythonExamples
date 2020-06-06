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
PUBLIC_IP_PREFIX_NAME = "myPublicIpPrefix"


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
# /PublicIPPrefixes/put/Create public IP prefix defaults[put]
#--------------------------------------------------------------------------
print("Create public IP prefix defaults")
BODY = {
  "location": AZURE_LOCATION,
  "sku": {
    "name": "Standard"
  },
  "prefix_length": "30"
}
result = mgmt_client.public_ip_prefixes.create_or_update(resource_group_name=RESOURCE_GROUP, public_ip_prefix_name=PUBLIC_IP_PREFIX_NAME, parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /PublicIPPrefixes/put/Create public IP prefix allocation method[put]
#--------------------------------------------------------------------------
print("Create public IP prefix allocation method")
BODY = {
  "zones": [
    "1"
  ],
  "location": AZURE_LOCATION
}
#result = mgmt_client.public_ip_prefixes.create_or_update(resource_group_name=RESOURCE_GROUP, public_ip_prefix_name=PUBLIC_IP_PREFIX_NAME, parameters=BODY)
#result = result.result()


#--------------------------------------------------------------------------
# /PublicIPPrefixes/get/Get public IP prefix[get]
#--------------------------------------------------------------------------
print("Get public IP prefix")
result = mgmt_client.public_ip_prefixes.get(resource_group_name=RESOURCE_GROUP, public_ip_prefix_name=PUBLIC_IP_PREFIX_NAME)


#--------------------------------------------------------------------------
# /PublicIPPrefixes/get/List resource group public IP prefixes[get]
#--------------------------------------------------------------------------
print("List resource group public IP prefixes")
result = mgmt_client.public_ip_prefixes.list(resource_group_name=RESOURCE_GROUP)


#--------------------------------------------------------------------------
# /PublicIPPrefixes/get/List all public IP prefixes[get]
#--------------------------------------------------------------------------
print("List all public IP prefixes")
result = mgmt_client.public_ip_prefixes.list_all()


#--------------------------------------------------------------------------
# /PublicIPPrefixes/patch/Update public IP prefix tags[patch]
#--------------------------------------------------------------------------
print("Update public IP prefix tags")
TAGS = {
  "tag1": "value1",
  "tag2": "value2"
}
result = mgmt_client.public_ip_prefixes.update_tags(resource_group_name=RESOURCE_GROUP, public_ip_prefix_name=PUBLIC_IP_PREFIX_NAME, tags=TAGS)


#--------------------------------------------------------------------------
# /PublicIPPrefixes/delete/Delete public IP prefix[delete]
#--------------------------------------------------------------------------
print("Delete public IP prefix")
result = mgmt_client.public_ip_prefixes.delete(resource_group_name=RESOURCE_GROUP, public_ip_prefix_name=PUBLIC_IP_PREFIX_NAME)
result = result.result()
