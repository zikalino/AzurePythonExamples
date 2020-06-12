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
NETWORK_WATCHER_NAME = "myNetworkWatcher"
FLOW_LOG_NAME = "myFlowLog"
STORAGE_ACCOUNT_NAME = "mystoragerndxxx"


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
from azure.mgmt.storage import StorageManagementClient
storage_client = StorageManagementClient(credentials, SUBSCRIPTION_ID)


#--------------------------------------------------------------------------
# resource group (prerequisite)
#--------------------------------------------------------------------------
print("Creating Resource Group")
resource_client.resource_groups.create_or_update(resource_group_name=RESOURCE_GROUP, parameters={ 'location': AZURE_LOCATION })


#--------------------------------------------------------------------------
# storage (prerequisite)
#--------------------------------------------------------------------------
print("Prerequisite - Creating Storage")
BODY = {
  "sku": {
    "name": "Standard_GRS"
  },
  "kind": "StorageV2",
  "location": AZURE_LOCATION,
  "encryption": {
    "services": {
      "file": {
        "key_type": "Account",
        "enabled": True
      },
      "blob": {
        "key_type": "Account",
        "enabled": True
      }
    },
    "key_source": "Microsoft.Storage"
  }
}
result_create = storage_client.storage_accounts.create(
    RESOURCE_GROUP,
    STORAGE_ACCOUNT_NAME,
    BODY
)
result = result_create.result()


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
# /NetworkWatchers/put/Create network watcher[put]
#--------------------------------------------------------------------------
print("Create network watcher")
BODY = {
  "location": AZURE_LOCATION
}
result = mgmt_client.network_watchers.create_or_update(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, parameters=BODY)


#--------------------------------------------------------------------------
# /FlowLogs/put/Create or update flow log[put]
#--------------------------------------------------------------------------
print("Create or update flow log")
BODY = {
  "location": AZURE_LOCATION,
  "target_resource_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/networkSecurityGroups/" + NETWORK_SECURITY_GROUP_NAME,
  "storage_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Storage/storageAccounts/" + STORAGE_ACCOUNT_NAME,
  "enabled": True,
  "format": {
    "type": "JSON",
    "version": "1"
  }
}
result = mgmt_client.flow_logs.create_or_update(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, flow_log_name=FLOW_LOG_NAME, parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /FlowLogs/get/Get flow log[get]
#--------------------------------------------------------------------------
print("Get flow log")
result = mgmt_client.flow_logs.get(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, flow_log_name=FLOW_LOG_NAME)


#--------------------------------------------------------------------------
# /FlowLogs/get/List connection monitors[get]
#--------------------------------------------------------------------------
print("List connection monitors")
result = mgmt_client.flow_logs.list(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME)


#--------------------------------------------------------------------------
# /FlowLogs/delete/Delete flow log[delete]
#--------------------------------------------------------------------------
print("Delete flow log")
result = mgmt_client.flow_logs.delete(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, flow_log_name=FLOW_LOG_NAME)
result = result.result()
