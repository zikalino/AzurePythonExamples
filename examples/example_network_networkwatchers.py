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
AZURE_LOCATION = 'westus'
RESOURCE_GROUP = "myResourceGroup"
NETWORK_WATCHER_NAME = "myNetworkWatcher"


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
resource_client.resource_groups.create_or_update(resource_group_name=RESOURCE_GROUP, parameters={ 'location': "eastus" })


#--------------------------------------------------------------------------
# /NetworkWatchers/put/Create network watcher[put]
#--------------------------------------------------------------------------
print("Create network watcher")
BODY = {
  "location": AZURE_LOCATION
}
result = mgmt_client.network_watchers.create_or_update(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, parameters=BODY)


#--------------------------------------------------------------------------
# /NetworkWatchers/get/Get network watcher[get]
#--------------------------------------------------------------------------
print("Get network watcher")
result = mgmt_client.network_watchers.get(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME)


#--------------------------------------------------------------------------
# /NetworkWatchers/get/List network watchers[get]
#--------------------------------------------------------------------------
print("List network watchers")
result = mgmt_client.network_watchers.list(resource_group_name=RESOURCE_GROUP)


#--------------------------------------------------------------------------
# /NetworkWatchers/get/List all network watchers[get]
#--------------------------------------------------------------------------
print("List all network watchers")
result = mgmt_client.network_watchers.list_all()


#--------------------------------------------------------------------------
# /NetworkWatchers/post/Network configuration diagnostic[post]
#--------------------------------------------------------------------------
print("Network configuration diagnostic")
BODY = {
  #"target_resource_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Compute/virtualMachines/" + VIRTUAL_MACHINE_NAME,
  "profiles": [
    {
      "direction": "Inbound",
      "protocol": "TCP",
      "source": "10.1.0.4",
      "destination": "12.11.12.14",
      "destination_port": "12100"
    }
  ]
}
#result = mgmt_client.network_watchers.get_network_configuration_diagnostic(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, parameters=BODY)
#result = result.result()


#--------------------------------------------------------------------------
# /NetworkWatchers/post/Get troubleshoot result[post]
#--------------------------------------------------------------------------
print("Get troubleshoot result")
#result = mgmt_client.network_watchers.get_troubleshooting_result(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, target_resource_id="/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Compute/virtualMachines/" + VIRTUAL_MACHINE_NAME)
#result = result.result()


#--------------------------------------------------------------------------
# /NetworkWatchers/post/Get Azure Reachability Report[post]
#--------------------------------------------------------------------------
print("Get Azure Reachability Report")
BODY = {
  "provider_location": {
    "country": "United States",
    "state": "washington"
  },
  "providers": [
    "Frontier Communications of America, Inc. - ASN 5650"
  ],
  "azure_locations": [
    "West US"
  ],
  "start_time": "2017-09-07T00:00:00Z",
  "end_time": "2017-09-10T00:00:00Z"
}
result = mgmt_client.network_watchers.get_azure_reachability_report(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /NetworkWatchers/post/Get Available Providers List[post]
#--------------------------------------------------------------------------
print("Get Available Providers List")
BODY = {
  "azure_locations": [
    "West US"
  ],
  "country": "United States",
  "state": "washington",
  "city": "seattle"
}
result = mgmt_client.network_watchers.list_available_providers(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /NetworkWatchers/post/Get flow log status[post]
#--------------------------------------------------------------------------
print("Get flow log status")
#result = mgmt_client.network_watchers.get_flow_log_status(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, target_resource_id="/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/networkSecurityGroups/" + NETWORK_SECURITY_GROUP_NAME)
#result = result.result()


#--------------------------------------------------------------------------
# /NetworkWatchers/post/Get security group view[post]
#--------------------------------------------------------------------------
print("Get security group view")
#result = mgmt_client.network_watchers.get_vmsecurity_rules(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, target_resource_id="/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Compute/virtualMachines/" + VIRTUAL_MACHINE_NAME)
#result = result.result()


#--------------------------------------------------------------------------
# /NetworkWatchers/post/Check connectivity[post]
#--------------------------------------------------------------------------
print("Check connectivity")
BODY = {
#  "source": {
#    "resource_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Compute/virtualMachines/" + VIRTUAL_MACHINE_NAME
#  },
  "destination": {
    "address": "192.168.100.4",
    "port": "3389"
  },
  "preferred_ipversion": "IPv4"
}
#result = mgmt_client.network_watchers.check_connectivity(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, parameters=BODY)
#result = result.result()


#--------------------------------------------------------------------------
# /NetworkWatchers/post/Configure flow log[post]
#--------------------------------------------------------------------------
print("Configure flow log")
BODY = {
  #"target_resource_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/networkSecurityGroups/" + NETWORK_SECURITY_GROUP_NAME,
  #"storage_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Storage/storageAccounts/" + STORAGE_ACCOUNT_NAME,
  "enabled": True
}
#result = mgmt_client.network_watchers.set_flow_log_configuration(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, parameters=BODY)
#result = result.result()


#--------------------------------------------------------------------------
# /NetworkWatchers/post/Ip flow verify[post]
#--------------------------------------------------------------------------
print("Ip flow verify")
BODY = {
#  "target_resource_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Compute/virtualMachines/" + VIRTUAL_MACHINE_NAME,
  "direction": "Outbound",
  "protocol": "TCP",
  "local_port": "80",
  "remote_port": "80",
  "local_ip_address": "10.2.0.4",
  "remote_ip_address": "121.10.1.1"
}
#result = mgmt_client.network_watchers.verify_ipflow(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, parameters=BODY)
#result = result.result()


#--------------------------------------------------------------------------
# /NetworkWatchers/post/Get troubleshooting[post]
#--------------------------------------------------------------------------
print("Get troubleshooting")
BODY = {
#  "target_resource_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Compute/virtualMachines/" + VIRTUAL_MACHINE_NAME,
#  "storage_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Storage/storageAccounts/" + STORAGE_ACCOUNT_NAME,
  "storage_path": "https://st1.blob.core.windows.net/cn1"
}
#result = mgmt_client.network_watchers.get_troubleshooting(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, parameters=BODY)
#result = result.result()


#--------------------------------------------------------------------------
# /NetworkWatchers/post/Get Topology[post]
#--------------------------------------------------------------------------
print("Get Topology")
BODY = {
  "target_resource_group_name": "rg2"
}
result = mgmt_client.network_watchers.get_topology(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, parameters=BODY)


#--------------------------------------------------------------------------
# /NetworkWatchers/post/Get next hop[post]
#--------------------------------------------------------------------------
print("Get next hop")
BODY = {
 # "target_resource_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Compute/virtualMachines/" + VIRTUAL_MACHINE_NAME,
  "source_ip_address": "10.0.0.5",
  "destination_ip_address": "10.0.0.10",
#  "target_nic_resource_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/networkInterfaces/" + NETWORK_INTERFACE_NAME
}
#result = mgmt_client.network_watchers.get_next_hop(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, parameters=BODY)
#result = result.result()


#--------------------------------------------------------------------------
# /NetworkWatchers/patch/Update network watcher tags[patch]
#--------------------------------------------------------------------------
print("Update network watcher tags")
TAGS = {
  "tag1": "value1",
  "tag2": "value2"
}
result = mgmt_client.network_watchers.update_tags(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, tags=TAGS)


#--------------------------------------------------------------------------
# /NetworkWatchers/delete/Delete network watcher[delete]
#--------------------------------------------------------------------------
print("Delete network watcher")
result = mgmt_client.network_watchers.delete(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME)
result = result.result()
