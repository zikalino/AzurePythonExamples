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
NETWORK_SECURITY_GROUP_NAME = "myNetworkSecurityGroup"
SECURITY_RULE_NAME = "mySecurityRule"


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
# /NetworkSecurityGroups/put/Create network security group[put]
#--------------------------------------------------------------------------
print("Create network security group")
BODY = {
  "location": AZURE_LOCATION
}
result = mgmt_client.network_security_groups.create_or_update(resource_group_name=RESOURCE_GROUP, network_security_group_name=NETWORK_SECURITY_GROUP_NAME, parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /SecurityRules/put/Create security rule[put]
#--------------------------------------------------------------------------
print("Create security rule")
BODY = {
  "protocol": "*",
  "source_address_prefix": "10.0.0.0/8",
  "destination_address_prefix": "11.0.0.0/8",
  "access": "Deny",
  "destination_port_range": "8080",
  "source_port_range": "*",
  "priority": "100",
  "direction": "Outbound"
}
result = mgmt_client.security_rules.create_or_update(resource_group_name=RESOURCE_GROUP, network_security_group_name=NETWORK_SECURITY_GROUP_NAME, security_rule_name=SECURITY_RULE_NAME, security_rule_parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /SecurityRules/get/List network security rules in network security group[get]
#--------------------------------------------------------------------------
print("List network security rules in network security group")
result = mgmt_client.security_rules.list(resource_group_name=RESOURCE_GROUP, network_security_group_name=NETWORK_SECURITY_GROUP_NAME)


#--------------------------------------------------------------------------
# /SecurityRules/get/Get network security rule in network security group[get]
#--------------------------------------------------------------------------
print("Get network security rule in network security group")
result = mgmt_client.security_rules.get(resource_group_name=RESOURCE_GROUP, network_security_group_name=NETWORK_SECURITY_GROUP_NAME, security_rule_name=SECURITY_RULE_NAME)


#--------------------------------------------------------------------------
# /SecurityRules/delete/Delete network security rule from network security group[delete]
#--------------------------------------------------------------------------
print("Delete network security rule from network security group")
result = mgmt_client.security_rules.delete(resource_group_name=RESOURCE_GROUP, network_security_group_name=NETWORK_SECURITY_GROUP_NAME, security_rule_name=SECURITY_RULE_NAME)
result = result.result()
