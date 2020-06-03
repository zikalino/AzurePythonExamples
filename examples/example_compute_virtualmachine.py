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
VM_NAME = "myVm"
NETWORK_INTERFACE_NAME = "myNetworkInterface"
VIRTUAL_NETWORK_NAME = "myVirtualNetwork"
SUBNET_NAME = "mySubnet"


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
from azure.mgmt.network import NetworkManagementClient
network_client = NetworkManagementClient(credentials, SUBSCRIPTION_ID)


#--------------------------------------------------------------------------
# resource group (prerequisite)
#--------------------------------------------------------------------------
print("Creating Resource Group")
resource_client.resource_groups.create_or_update(resource_group_name=RESOURCE_GROUP, parameters={ 'location': AZURE_LOCATION })


#--------------------------------------------------------------------------
# virtual network (prerequisite)
#--------------------------------------------------------------------------
print("Prerequisite - Creating Virtual Network")
azure_operation_poller = network_client.virtual_networks.create_or_update(
    RESOURCE_GROUP,
    VIRTUAL_NETWORK_NAME,
    {
        'location': AZURE_LOCATION,
        'address_space': {
            'address_prefixes': ['10.0.0.0/16']
        }
    },
)
result_create = azure_operation_poller.result()

async_subnet_creation = network_client.subnets.create_or_update(
    RESOURCE_GROUP,
    VIRTUAL_NETWORK_NAME,
    SUBNET_NAME,
    {'address_prefix': '10.0.0.0/24'}
)
subnet_info = async_subnet_creation.result()


#--------------------------------------------------------------------------
# network interface (prerequisite)
#--------------------------------------------------------------------------
print("Prerequisite - Creating Network Interface")
async_nic_creation = network_client.network_interfaces.create_or_update(
    RESOURCE_GROUP,
    NETWORK_INTERFACE_NAME,
    {
        'location': AZURE_LOCATION,
        'ip_configurations': [{
            'name': 'MyIpConfig',
            'subnet': {
                'id': subnet_info.id
            }
        }]
    }
)
nic_info = async_nic_creation.result()


#--------------------------------------------------------------------------
# /VirtualMachines/put/Create a vm with password authentication.[put]
#--------------------------------------------------------------------------
print("Create a vm with password authentication.")
BODY = {
  "location": AZURE_LOCATION,
  "hardware_profile": {
    "vm_size": "Standard_D1_v2"
  },
  "storage_profile": {
    "image_reference": {
      "sku": "2016-Datacenter",
      "publisher": "MicrosoftWindowsServer",
      "version": "latest",
      "offer": "WindowsServer"
    },
    "os_disk": {
      "caching": "ReadWrite",
      "managed_disk": {
        "storage_account_type": "Standard_LRS"
      },
      "name": "myVMosdisk",
      "create_option": "FromImage"
    }
  },
  "os_profile": {
    "admin_username": "myuser",
    "computer_name": "myVM",
    "admin_password": "Password123!!!"
  },
  "network_profile": {
    "network_interfaces": [
      {
        "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/networkInterfaces/" + NETWORK_INTERFACE_NAME,
        "properties": {
          "primary": True
        }
      }
    ]
  }
}
result = mgmt_client.virtual_machines.create_or_update(resource_group_name=RESOURCE_GROUP, vm_name=VM_NAME, parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /VirtualMachines/get/Get Virtual Machine Instance View.[get]
#--------------------------------------------------------------------------
print("Get Virtual Machine Instance View.")
result = mgmt_client.virtual_machines.instance_view(resource_group_name=RESOURCE_GROUP, vm_name=VM_NAME)


#--------------------------------------------------------------------------
# /VirtualMachines/get/Lists all available virtual machine sizes to which the specified virtual machine can be resized[get]
#--------------------------------------------------------------------------
print("Lists all available virtual machine sizes to which the specified virtual machine can be resized")
result = mgmt_client.virtual_machines.list_available_sizes(resource_group_name=RESOURCE_GROUP, vm_name=VM_NAME)


#--------------------------------------------------------------------------
# /VirtualMachines/get/Get a Virtual Machine.[get]
#--------------------------------------------------------------------------
print("Get a Virtual Machine.")
result = mgmt_client.virtual_machines.get(resource_group_name=RESOURCE_GROUP, vm_name=VM_NAME)


#--------------------------------------------------------------------------
# /VirtualMachines/get/Lists all the virtual machines under the specified subscription for the specified location.[get]
#--------------------------------------------------------------------------
print("Lists all the virtual machines under the specified subscription for the specified location.")
result = mgmt_client.virtual_machines.list_by_location(location=AZURE_LOCATION)
