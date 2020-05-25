#-------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#--------------------------------------------------------------------------

import os
from azure.mgmt.mixedreality import MixedRealityClient
from azure.mgmt.resource import ResourceManagementClient
from azure.common.credentials import ServicePrincipalCredentials

AZURE_LOCATION = 'eastus'
RESOURCE_GROUP = "myResourceGroup"

# credentials from environment
SUBSCRIPTION_ID = os.environ['AZURE_SUBSCRIPTION_ID']
TENANT_ID = os.environ['AZURE_TENANT']
CLIENT_ID = os.environ['AZURE_CLIENT_ID']
CLIENT_SECRET = os.environ['AZURE_SECRET']
ACCOUNT_NAME = "mySpatialAccountNameXyz"

# management client
credentials = ServicePrincipalCredentials(
    client_id=CLIENT_ID,
    secret=CLIENT_SECRET,
    tenant=TENANT_ID
)
mgmt_client = MixedRealityClient(credentials, SUBSCRIPTION_ID)

resource_management_client = ResourceManagementClient(credentials, SUBSCRIPTION_ID);

# CREATE RESOURCE GROUP

print("Creating Resource Group")
resource_management_client.resource_groups.create_or_update(resource_group_name=RESOURCE_GROUP, parameters={ 'location': AZURE_LOCATION })

# /SpatialAnchorsAccounts/put/Create spatial anchor account[put]
print("Create spatial anchor account")
BODY = {
  "location": AZURE_LOCATION
}
result = mgmt_client.spatial_anchors_accounts.create(resource_group_name=RESOURCE_GROUP, account_name=ACCOUNT_NAME, location=AZURE_LOCATION)

# /RemoteRenderingAccounts/put/Create remote rendering account[put]
print("Create remote rendering account")
BODY = {
  "identity": {
    "type": "SystemAssigned"
  },
  "location": AZURE_LOCATION
}
result = mgmt_client.remote_rendering_accounts.create(resource_group_name=RESOURCE_GROUP, account_name=ACCOUNT_NAME, remote_rendering_account=BODY)

# /RemoteRenderingAccounts/get/Get remote rendering account[get]
print("Get remote rendering account")
result = mgmt_client.remote_rendering_accounts.get(resource_group_name=RESOURCE_GROUP, account_name=ACCOUNT_NAME)

# /SpatialAnchorsAccounts/get/Get spatial anchors account[get]
print("Get spatial anchors account")
result = mgmt_client.spatial_anchors_accounts.get(resource_group_name=RESOURCE_GROUP, account_name=ACCOUNT_NAME)

# /RemoteRenderingAccounts/get/List remote rendering accounts by resource group[get]
print("List remote rendering accounts by resource group")
result = mgmt_client.remote_rendering_accounts.list_by_resource_group(resource_group_name=RESOURCE_GROUP)

# /SpatialAnchorsAccounts/get/List spatial anchor accounts by resource group[get]
print("List spatial anchor accounts by resource group")
result = mgmt_client.spatial_anchors_accounts.list_by_resource_group(resource_group_name=RESOURCE_GROUP)

# /RemoteRenderingAccounts/get/List remote rendering accounts by subscription[get]
print("List remote rendering accounts by subscription")
result = mgmt_client.remote_rendering_accounts.list_by_subscription()

# /SpatialAnchorsAccounts/get/List spatial anchors accounts by subscription[get]
print("List spatial anchors accounts by subscription")
result = mgmt_client.spatial_anchors_accounts.list_by_subscription()

# /Operations/get/List available operations[get]
print("List available operations")
result = mgmt_client.operations.list()

# /RemoteRenderingAccounts/post/Regenerate remote rendering account keys[post]
print("Regenerate remote rendering account keys")
BODY = {
  "serial": "1"
}
result = mgmt_client.remote_rendering_accounts.regenerate_keys(resource_group_name=RESOURCE_GROUP, account_name=ACCOUNT_NAME, regenerate=BODY)

# /SpatialAnchorsAccounts/post/Regenerate spatial anchors account keys[post]
print("Regenerate spatial anchors account keys")
BODY = {
  "serial": "1"
}
result = mgmt_client.spatial_anchors_accounts.regenerate_keys(resource_group_name=RESOURCE_GROUP, account_name=ACCOUNT_NAME, regenerate=BODY)

# /RemoteRenderingAccounts/patch/Update remote rendering account[patch]
print("Update remote rendering account")
BODY = {
  "identity": {
    "type": "SystemAssigned"
  },
  "location": AZURE_LOCATION,
  "tags": {
    "heroine": "juliet",
    "hero": "romeo"
  }
}
result = mgmt_client.remote_rendering_accounts.update(resource_group_name=RESOURCE_GROUP, account_name=ACCOUNT_NAME, remote_rendering_account=BODY)

# /SpatialAnchorsAccounts/patch/Update spatial anchors account[patch]
print("Update spatial anchors account")
TAGS = {
  "heroine": "juliet",
  "hero": "romeo"
}
result = mgmt_client.spatial_anchors_accounts.update(resource_group_name=RESOURCE_GROUP, account_name=ACCOUNT_NAME, location=AZURE_LOCATION, tags=TAGS)

# //post/CheckLocalNameAvailability[post]
print("CheckLocalNameAvailability")
result = mgmt_client.check_name_availability_local(azure_location=AZURE_LOCATION, location=AZURE_LOCATION, name="MyAccount", type="Microsoft.MixedReality/spatialAnchorsAccounts")

# /RemoteRenderingAccounts/delete/Delete remote rendering account[delete]
print("Delete remote rendering account")
result = mgmt_client.remote_rendering_accounts.delete(resource_group_name=RESOURCE_GROUP, account_name=ACCOUNT_NAME)

# /SpatialAnchorsAccounts/delete/Delete spatial anchors account[delete]
print("Delete spatial anchors account")
result = mgmt_client.spatial_anchors_accounts.delete(resource_group_name=RESOURCE_GROUP, account_name=ACCOUNT_NAME)
