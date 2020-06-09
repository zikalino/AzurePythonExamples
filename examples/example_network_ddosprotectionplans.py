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
DDOS_PROTECTION_PLAN_NAME = "myDdosProtectionPlan"


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
# /DdosProtectionPlans/put/Create DDoS protection plan[put]
#--------------------------------------------------------------------------
print("Create DDoS protection plan")
result = mgmt_client.ddos_protection_plans.create_or_update(resource_group_name=RESOURCE_GROUP, ddos_protection_plan_name=DDOS_PROTECTION_PLAN_NAME, location=AZURE_LOCATION)
result = result.result()


#--------------------------------------------------------------------------
# /DdosProtectionPlans/get/Get DDoS protection plan[get]
#--------------------------------------------------------------------------
print("Get DDoS protection plan")
result = mgmt_client.ddos_protection_plans.get(resource_group_name=RESOURCE_GROUP, ddos_protection_plan_name=DDOS_PROTECTION_PLAN_NAME)


#--------------------------------------------------------------------------
# /DdosProtectionPlans/get/List DDoS protection plans in resource group[get]
#--------------------------------------------------------------------------
print("List DDoS protection plans in resource group")
result = mgmt_client.ddos_protection_plans.list_by_resource_group(resource_group_name=RESOURCE_GROUP)


#--------------------------------------------------------------------------
# /DdosProtectionPlans/get/List all DDoS protection plans[get]
#--------------------------------------------------------------------------
print("List all DDoS protection plans")
result = mgmt_client.ddos_protection_plans.list()


#--------------------------------------------------------------------------
# /DdosProtectionPlans/patch/DDoS protection plan Update tags[patch]
#--------------------------------------------------------------------------
print("DDoS protection plan Update tags")
TAGS = {
  "tag1": "value1",
  "tag2": "value2"
}
result = mgmt_client.ddos_protection_plans.update_tags(resource_group_name=RESOURCE_GROUP, ddos_protection_plan_name=DDOS_PROTECTION_PLAN_NAME, tags=TAGS)


#--------------------------------------------------------------------------
# /DdosProtectionPlans/delete/Delete DDoS protection plan[delete]
#--------------------------------------------------------------------------
print("Delete DDoS protection plan")
result = mgmt_client.ddos_protection_plans.delete(resource_group_name=RESOURCE_GROUP, ddos_protection_plan_name=DDOS_PROTECTION_PLAN_NAME)
result = result.result()
