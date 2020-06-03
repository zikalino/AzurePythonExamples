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
AVAILABILITY_SET_NAME = "myAvailabilitySet"


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
# /AvailabilitySets/put/Create an availability set.[put]
#--------------------------------------------------------------------------
print("Create an availability set.")
BODY = {
  "location": AZURE_LOCATION,
  "platform_fault_domain_count": "2",
  "platform_update_domain_count": "20"
}
result = mgmt_client.availability_sets.create_or_update(resource_group_name=RESOURCE_GROUP, availability_set_name=AVAILABILITY_SET_NAME, parameters=BODY)


#--------------------------------------------------------------------------
# /AvailabilitySets/get/List availability sets in a subscription.[get]
#--------------------------------------------------------------------------
print("List availability sets in a subscription.")
result = mgmt_client.availability_sets.list_by_subscription(expand="virtualMachines\$ref")
