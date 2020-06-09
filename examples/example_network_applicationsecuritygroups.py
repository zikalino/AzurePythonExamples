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
APPLICATION_SECURITY_GROUP_NAME = "myApplicationSecurityGroup"


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
# /ApplicationSecurityGroups/put/Create application security group[put]
#--------------------------------------------------------------------------
print("Create application security group")
BODY = {
  "location": AZURE_LOCATION
}
result = mgmt_client.application_security_groups.create_or_update(resource_group_name=RESOURCE_GROUP, application_security_group_name=APPLICATION_SECURITY_GROUP_NAME, parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /ApplicationSecurityGroups/get/Get application security group[get]
#--------------------------------------------------------------------------
print("Get application security group")
result = mgmt_client.application_security_groups.get(resource_group_name=RESOURCE_GROUP, application_security_group_name=APPLICATION_SECURITY_GROUP_NAME)


#--------------------------------------------------------------------------
# /ApplicationSecurityGroups/get/List load balancers in resource group[get]
#--------------------------------------------------------------------------
print("List load balancers in resource group")
result = mgmt_client.application_security_groups.list(resource_group_name=RESOURCE_GROUP)


#--------------------------------------------------------------------------
# /ApplicationSecurityGroups/get/List all application security groups[get]
#--------------------------------------------------------------------------
print("List all application security groups")
result = mgmt_client.application_security_groups.list_all()


#--------------------------------------------------------------------------
# /ApplicationSecurityGroups/patch/Update application security group tags[patch]
#--------------------------------------------------------------------------
print("Update application security group tags")
TAGS = {
  "tag1": "value1",
  "tag2": "value2"
}
result = mgmt_client.application_security_groups.update_tags(resource_group_name=RESOURCE_GROUP, application_security_group_name=APPLICATION_SECURITY_GROUP_NAME, tags=TAGS)


#--------------------------------------------------------------------------
# /ApplicationSecurityGroups/delete/Delete application security group[delete]
#--------------------------------------------------------------------------
print("Delete application security group")
result = mgmt_client.application_security_groups.delete(resource_group_name=RESOURCE_GROUP, application_security_group_name=APPLICATION_SECURITY_GROUP_NAME)
result = result.result()
