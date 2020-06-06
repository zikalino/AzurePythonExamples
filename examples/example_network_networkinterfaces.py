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
NETWORK_INTERFACE_NAME = "myNetworkInterface"
PUBLIC_IP_ADDRESS_NAME = "myPublicIpAddress"
VIRTUAL_NETWORK_NAME = "myVirtualNetwork"
SUBNET_NAME = "mySubnet"
VIRTUAL_MACHINE_SCALE_SET_NAME = "myVirtualMachineScaleSet"
VIRTUALMACHINE_INDEX = "myVirtualmachineIndex"
IP_CONFIGURATION_NAME = "myIpConfiguration"
VIRTUAL_MACHINE_NAME = "myVirtualMachine"


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
from azure.mgmt.compute import ComputeManagementClient
compute_client = ComputeManagementClient(credentials, SUBSCRIPTION_ID)


#--------------------------------------------------------------------------
# resource group (prerequisite)
#--------------------------------------------------------------------------
print("Creating Resource Group")
resource_client.resource_groups.create_or_update(resource_group_name=RESOURCE_GROUP, parameters={ 'location': AZURE_LOCATION })


#--------------------------------------------------------------------------
# virtual machine (prerequisite)
#--------------------------------------------------------------------------
print("Prerequisite - Creating Virtual Machine")
# Create a vm with empty data disks.[put]
BODY = {
  "location": AZURE_LOCATION,
  "hardware_profile": {
    "vm_size": "Standard_D2_v2"
  },
  "storage_profile": {
    "image_reference": {
      "sku": "enterprise",
      "publisher": "microsoftsqlserver",
      "version": "latest",
      "offer": "sql2019-ws2019"
    },
    "os_disk": {
      "caching": "ReadWrite",
      "managed_disk": {
        "storage_account_type": "Standard_LRS"
      },
      "name": "myVMosdisk",
      "create_option": "FromImage"
    },
    "data_disks": [
      {
        "disk_size_gb": "1023",
        "create_option": "Empty",
        "lun": "0"
      },
      {
        "disk_size_gb": "1023",
        "create_option": "Empty",
        "lun": "1"
      }
    ]
  },
  "os_profile": {
    "admin_username": "testuser",
    "admin_password": "Password1!!!",
    "computer_name" : "myvm"
  },
  "network_profile": {
    "network_interfaces": [
      {
        # "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/networkInterfaces/" + NIC_ID + "",
#        "id": nic_id,
        "properties": {
          "primary": True
        }
      }
    ]
  }
}
#result = compute_client.virtual_machines.create_or_update(RESOURCE_GROUP, vm_name, BODY)
#result = result.result()


#--------------------------------------------------------------------------
# /VirtualNetworks/put/Create virtual network[put]
#--------------------------------------------------------------------------
print("Create virtual network")
BODY = {
  "address_space": {
    "address_prefixes": [
      "10.0.0.0/16"
    ]
  },
  "location": AZURE_LOCATION
}
result = mgmt_client.virtual_networks.create_or_update(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME, parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /Subnets/put/Create subnet[put]
#--------------------------------------------------------------------------
print("Create subnet")
BODY = {
  "address_prefix": "10.0.0.0/16"
}
result = mgmt_client.subnets.create_or_update(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME, subnet_name=SUBNET_NAME, subnet_parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /PublicIPAddresses/put/Create public IP address defaults[put]
#--------------------------------------------------------------------------
print("Create public IP address defaults")
BODY = {
  "location": AZURE_LOCATION
}
result = mgmt_client.public_ip_addresses.create_or_update(resource_group_name=RESOURCE_GROUP, public_ip_address_name=PUBLIC_IP_ADDRESS_NAME, parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /NetworkInterfaces/put/Create network interface[put]
#--------------------------------------------------------------------------
print("Create network interface")
BODY = {
  "enable_accelerated_networking": True,
  "ip_configurations": [
    {
      "name": "ipconfig1",
      "properties": {
        "public_ip_address": {
          "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/publicIPAddresses/" + PUBLIC_IP_ADDRESS_NAME
        },
        "subnet": {
          "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualNetworks/" + VIRTUAL_NETWORK_NAME + "/subnets/" + SUBNET_NAME
        }
      }
    }
  ],
  "location": AZURE_LOCATION
}
result = mgmt_client.network_interfaces.create_or_update(resource_group_name=RESOURCE_GROUP, network_interface_name=NETWORK_INTERFACE_NAME, parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /NetworkInterfaces/get/Get virtual machine scale set network interface[get]
#--------------------------------------------------------------------------
print("Get virtual machine scale set network interface")
#result = mgmt_client.network_interfaces.get_virtual_machine_scale_set_network_interface(resource_group_name=RESOURCE_GROUP, virtual_machine_scale_set_name=VIRTUAL_MACHINE_SCALE_SET_NAME, virtualmachine_index=VIRTUALMACHINE_INDEX, network_interface_name=NETWORK_INTERFACE_NAME)


#--------------------------------------------------------------------------
# /NetworkInterfaces/get/List virtual machine scale set network interface ip configurations[get]
#--------------------------------------------------------------------------
print("List virtual machine scale set network interface ip configurations")
#result = mgmt_client.network_interfaces.list_virtual_machine_scale_set_ip_configurations(resource_group_name=RESOURCE_GROUP, virtual_machine_scale_set_name=VIRTUAL_MACHINE_SCALE_SET_NAME, virtualmachine_index=VIRTUALMACHINE_INDEX, network_interface_name=NETWORK_INTERFACE_NAME)


#--------------------------------------------------------------------------
# /NetworkInterfaces/get/Get virtual machine scale set network interface[get]
#--------------------------------------------------------------------------
print("Get virtual machine scale set network interface")
#result = mgmt_client.network_interfaces.get_virtual_machine_scale_set_network_interface(resource_group_name=RESOURCE_GROUP, virtual_machine_scale_set_name=VIRTUAL_MACHINE_SCALE_SET_NAME, virtualmachine_index=VIRTUALMACHINE_INDEX, network_interface_name=NETWORK_INTERFACE_NAME)


#--------------------------------------------------------------------------
# /NetworkInterfaces/get/List virtual machine scale set vm network interfaces[get]
#--------------------------------------------------------------------------
print("List virtual machine scale set vm network interfaces")
#result = mgmt_client.network_interfaces.list_virtual_machine_scale_set_vmnetwork_interfaces(resource_group_name=RESOURCE_GROUP, virtual_machine_scale_set_name=VIRTUAL_MACHINE_SCALE_SET_NAME, virtualmachine_index=VIRTUALMACHINE_INDEX)


#--------------------------------------------------------------------------
# /NetworkInterfaces/get/List virtual machine scale set network interfaces[get]
#--------------------------------------------------------------------------
print("List virtual machine scale set network interfaces")
#result = mgmt_client.network_interfaces.list_virtual_machine_scale_set_network_interfaces(resource_group_name=RESOURCE_GROUP, virtual_machine_scale_set_name=VIRTUAL_MACHINE_SCALE_SET_NAME)


#--------------------------------------------------------------------------
# /NetworkInterfaces/get/Get network interface[get]
#--------------------------------------------------------------------------
print("Get network interface")
result = mgmt_client.network_interfaces.get(resource_group_name=RESOURCE_GROUP, network_interface_name=NETWORK_INTERFACE_NAME)


#--------------------------------------------------------------------------
# /NetworkInterfaces/get/List network interfaces in resource group[get]
#--------------------------------------------------------------------------
print("List network interfaces in resource group")
result = mgmt_client.network_interfaces.list(resource_group_name=RESOURCE_GROUP)


#--------------------------------------------------------------------------
# /NetworkInterfaces/get/List all network interfaces[get]
#--------------------------------------------------------------------------
print("List all network interfaces")
result = mgmt_client.network_interfaces.list_all()


#--------------------------------------------------------------------------
# /NetworkInterfaces/post/List network interface effective network security groups[post]
#--------------------------------------------------------------------------
print("List network interface effective network security groups")
#result = mgmt_client.network_interfaces.list_effective_network_security_groups(resource_group_name=RESOURCE_GROUP, network_interface_name=NETWORK_INTERFACE_NAME)
#result = result.result()


#--------------------------------------------------------------------------
# /NetworkInterfaces/post/Show network interface effective route tables[post]
#--------------------------------------------------------------------------
print("Show network interface effective route tables")
#result = mgmt_client.network_interfaces.get_effective_route_table(resource_group_name=RESOURCE_GROUP, network_interface_name=NETWORK_INTERFACE_NAME)
#result = result.result()


#--------------------------------------------------------------------------
# /NetworkInterfaces/patch/Update network interface tags[patch]
#--------------------------------------------------------------------------
print("Update network interface tags")
TAGS = {
  "tag1": "value1",
  "tag2": "value2"
}
result = mgmt_client.network_interfaces.update_tags(resource_group_name=RESOURCE_GROUP, network_interface_name=NETWORK_INTERFACE_NAME, tags=TAGS)


#--------------------------------------------------------------------------
# /NetworkInterfaces/delete/Delete network interface[delete]
#--------------------------------------------------------------------------
print("Delete network interface")
result = mgmt_client.network_interfaces.delete(resource_group_name=RESOURCE_GROUP, network_interface_name=NETWORK_INTERFACE_NAME)
result = result.result()
