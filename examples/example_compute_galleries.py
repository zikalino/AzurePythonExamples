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
IMAGE_NAME = "myImage"
DISK_NAME = "myDisk"
GALLERY_NAME = "myGallery"
GALLERY_IMAGE_NAME = "myGalleryImage"
GALLERY_IMAGE_VERSION_NAME = "1.0.0"
DISK_ENCRYPTION_SET_NAME = "myDiskEncryptionSet"


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
# /Disks/put/Create an empty managed disk.[put]
#--------------------------------------------------------------------------
print("Create an empty managed disk.")
BODY = {
  "location": AZURE_LOCATION,
  "creation_data": {
    "create_option": "Empty"
  },
  "disk_size_gb": "200"
}
result = mgmt_client.disks.create_or_update(resource_group_name=RESOURCE_GROUP, disk_name=DISK_NAME, disk=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /Images/put/Create a virtual machine image from a managed disk.[put]
#--------------------------------------------------------------------------
print("Create a virtual machine image from a managed disk.")
BODY = {
  "location": AZURE_LOCATION,
  "storage_profile": {
    "os_disk": {
      "os_type": "Linux",
      "managed_disk": {
        "id": "subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Compute/disks/" + DISK_NAME
      },
      "os_state": "Generalized"
    },
    "zone_resilient": True
  },
  "hyper_vgeneration": "V1"
}
result = mgmt_client.images.create_or_update(resource_group_name=RESOURCE_GROUP, image_name=IMAGE_NAME, parameters=BODY)
result = result.result()


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
# /GalleryImages/put/Create or update a simple gallery image.[put]
#--------------------------------------------------------------------------
print("Create or update a simple gallery image.")
BODY = {
  "location": AZURE_LOCATION,
  "os_type": "Linux",
  "os_state": "Generalized",
  "hyper_vgeneration": "V1",
  "identifier": {
    "publisher": "myPublisherName",
    "offer": "myOfferName",
    "sku": "mySkuName"
  }
}
result = mgmt_client.gallery_images.create_or_update(resource_group_name=RESOURCE_GROUP, gallery_name=GALLERY_NAME, gallery_image_name=GALLERY_IMAGE_NAME, gallery_image=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /GalleryImageVersions/put/Create or update a simple Gallery Image Version (Managed Image as source).[put]
#--------------------------------------------------------------------------
print("Create or update a simple Gallery Image Version (Managed Image as source).")
BODY = {
  "location": AZURE_LOCATION,
  "publishing_profile": {
    "target_regions": [
      {
        "name": "West US",
        "regional_replica_count": "1"# ,
        #"encryption": {
          #"os_disk_image": {
          #  #"disk_encryption_set_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Compute/diskEncryptionSet/" + DISK_ENCRYPTION_SET_NAME
          #},
          #"data_disk_images": [
          #  {
          #    "lun": "0"#,
          #    #"disk_encryption_set_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Compute/diskEncryptionSet/" + DISK_ENCRYPTION_SET_NAME
          #  },
          #  {
          #    "lun": "1"#,
              #"disk_encryption_set_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Compute/diskEncryptionSet/" + DISK_ENCRYPTION_SET_NAME
          #  }
          #]
        #}
      },
      {
        "name": "East US",
        "regional_replica_count": "2",
        "storage_account_type": "Standard_ZRS"
      }
    ]
  },
  "storage_profile": {
    "source": {
      "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Compute/images/" + IMAGE_NAME
    }
  }
}
result = mgmt_client.gallery_image_versions.create_or_update(resource_group_name=RESOURCE_GROUP, gallery_name=GALLERY_NAME, gallery_image_name=GALLERY_IMAGE_NAME, gallery_image_version_name=GALLERY_IMAGE_VERSION_NAME, gallery_image_version=BODY)
result = result.result()








#--------------------------------------------------------------------------
# /GalleryImageVersions/get/Get a gallery Image Version.[get]
#--------------------------------------------------------------------------
print("Get a gallery Image Version.")
result = mgmt_client.gallery_image_versions.get(resource_group_name=RESOURCE_GROUP, gallery_name=GALLERY_NAME, gallery_image_name=GALLERY_IMAGE_NAME, gallery_image_version_name=GALLERY_IMAGE_VERSION_NAME)


#--------------------------------------------------------------------------
# /GalleryImageVersions/get/List gallery Image Versions in a gallery Image Definition.[get]
#--------------------------------------------------------------------------
print("List gallery Image Versions in a gallery Image Definition.")
result = mgmt_client.gallery_image_versions.list_by_gallery_image(resource_group_name=RESOURCE_GROUP, gallery_name=GALLERY_NAME, gallery_image_name=GALLERY_IMAGE_NAME)


#--------------------------------------------------------------------------
# /GalleryImages/get/Get a gallery image.[get]
#--------------------------------------------------------------------------
print("Get a gallery image.")
result = mgmt_client.gallery_images.get(resource_group_name=RESOURCE_GROUP, gallery_name=GALLERY_NAME, gallery_image_name=GALLERY_IMAGE_NAME)


#--------------------------------------------------------------------------
# /GalleryImages/get/List gallery images in a gallery.[get]
#--------------------------------------------------------------------------
print("List gallery images in a gallery.")
result = mgmt_client.gallery_images.list_by_gallery(resource_group_name=RESOURCE_GROUP, gallery_name=GALLERY_NAME)


#--------------------------------------------------------------------------
# /GalleryImageVersions/patch/Update a simple Gallery Image Version (Managed Image as source).[patch]
#--------------------------------------------------------------------------
print("Update a simple Gallery Image Version (Managed Image as source).")
BODY = {
  "publishing_profile": {
    "target_regions": [
      {
        "name": "West US",
        "regional_replica_count": "1"
      },
      {
        "name": "East US",
        "regional_replica_count": "2",
        "storage_account_type": "Standard_ZRS"
      }
    ]
  },
  "storage_profile": {
    "source": {
      "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Compute/images/" + IMAGE_NAME
    }
  }
}
result = mgmt_client.gallery_image_versions.update(resource_group_name=RESOURCE_GROUP, gallery_name=GALLERY_NAME, gallery_image_name=GALLERY_IMAGE_NAME, gallery_image_version_name=GALLERY_IMAGE_VERSION_NAME, gallery_image_version=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /GalleryImages/patch/Update a simple gallery image.[patch]
#--------------------------------------------------------------------------
print("Update a simple gallery image.")
BODY = {
  "os_type": "Linux",
  "os_state": "Generalized",
  "hyper_vgeneration": "V1",
  "identifier": {
    "publisher": "myPublisherName",
    "offer": "myOfferName",
    "sku": "mySkuName"
  }
}
result = mgmt_client.gallery_images.update(resource_group_name=RESOURCE_GROUP, gallery_name=GALLERY_NAME, gallery_image_name=GALLERY_IMAGE_NAME, gallery_image=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /GalleryImageVersions/delete/Delete a gallery Image Version.[delete]
#--------------------------------------------------------------------------
print("Delete a gallery Image Version.")
result = mgmt_client.gallery_image_versions.delete(resource_group_name=RESOURCE_GROUP, gallery_name=GALLERY_NAME, gallery_image_name=GALLERY_IMAGE_NAME, gallery_image_version_name=GALLERY_IMAGE_VERSION_NAME)
result = result.result()


#--------------------------------------------------------------------------
# /GalleryImages/delete/Delete a gallery image.[delete]
#--------------------------------------------------------------------------
print("Delete a gallery image.")
result = mgmt_client.gallery_images.delete(resource_group_name=RESOURCE_GROUP, gallery_name=GALLERY_NAME, gallery_image_name=GALLERY_IMAGE_NAME)
# result = result.result()


#--------------------------------------------------------------------------
# /Galleries/delete/Delete a gallery.[delete]
#--------------------------------------------------------------------------
print("Delete a gallery.")
result = mgmt_client.galleries.delete(resource_group_name=RESOURCE_GROUP, gallery_name=GALLERY_NAME)
# result = result.result()
