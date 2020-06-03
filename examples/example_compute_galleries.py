#-------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#--------------------------------------------------------------------------

import os
from azure.mgmt.compute import ComputeManagementClient
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
GALLERY_NAME = "myGallery"


#--------------------------------------------------------------------------
# management clients
#--------------------------------------------------------------------------
credentials = ServicePrincipalCredentials(
    client_id=CLIENT_ID,
    secret=CLIENT_SECRET,
    tenant=TENANT_ID
)
mgmt_client = ComputeManagementClient(credentials, SUBSCRIPTION_ID)
resource_client = ResourceManagementClient(credentials, SUBSCRIPTION_ID)


#--------------------------------------------------------------------------
# resource group (prerequisite)
#--------------------------------------------------------------------------
print("Creating Resource Group")
resource_client.resource_groups.create_or_update(resource_group_name=RESOURCE_GROUP, parameters={ 'location': AZURE_LOCATION })


#--------------------------------------------------------------------------
# /Galleries/put/Create or update a simple gallery.[put]
#--------------------------------------------------------------------------
print("Create or update a simple gallery.")
BODY = {
  "location": AZURE_LOCATION,
  "description": "This is the gallery description."
}
result = mgmt_client.galleries.create_or_update(resource_group_name=RESOURCE_GROUP, gallery_name=GALLERY_NAME, gallery=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /Galleries/get/Get a gallery.[get]
#--------------------------------------------------------------------------
print("Get a gallery.")
result = mgmt_client.galleries.get(resource_group_name=RESOURCE_GROUP, gallery_name=GALLERY_NAME)


#--------------------------------------------------------------------------
# /Galleries/get/List galleries in a resource group.[get]
#--------------------------------------------------------------------------
print("List galleries in a resource group.")
result = mgmt_client.galleries.list_by_resource_group(resource_group_name=RESOURCE_GROUP)


#--------------------------------------------------------------------------
# /Galleries/get/List galleries in a subscription.[get]
#--------------------------------------------------------------------------
print("List galleries in a subscription.")
result = mgmt_client.galleries.list()


#--------------------------------------------------------------------------
# /Galleries/patch/Update a simple gallery.[patch]
#--------------------------------------------------------------------------
print("Update a simple gallery.")
BODY = {
  "description": "This is the gallery description."
}
result = mgmt_client.galleries.update(resource_group_name=RESOURCE_GROUP, gallery_name=GALLERY_NAME, gallery=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /Galleries/delete/Delete a gallery.[delete]
#--------------------------------------------------------------------------
print("Delete a gallery.")
result = mgmt_client.galleries.delete(resource_group_name=RESOURCE_GROUP, gallery_name=GALLERY_NAME)
result = result.result()
