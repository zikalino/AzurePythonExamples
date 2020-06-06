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
PUBLIC_IP_ADDRESS_NAME = "myPublicIpAddress"
VIRTUAL_MACHINE_SCALE_SET_NAME = "myVirtualMachineScaleSet"
VIRTUALMACHINE_INDEX = "myVirtualmachineIndex"
NETWORK_INTERFACE_NAME = "myNetworkInterface"
IP_CONFIGURATION_NAME = "myIpConfiguration"
VIRTUAL_MACHINE_NAME = "myVirtualMachine"
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
 #       "id": nic_id,
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
# /PublicIPAddresses/put/Create public IP address DNS[put]
#--------------------------------------------------------------------------
print("Create public IP address DNS")
BODY = {
  "properties": {
    "dns_settings": {
      "domain_name_label": "dnslbl"
    }
  },
  "location": AZURE_LOCATION
}
result = mgmt_client.public_ip_addresses.create_or_update(resource_group_name=RESOURCE_GROUP, public_ip_address_name=PUBLIC_IP_ADDRESS_NAME, parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /PublicIPAddresses/put/Create public IP address allocation method[put]
#--------------------------------------------------------------------------
print("Create public IP address allocation method")
[
  "1"
]
result = mgmt_client.public_ip_addresses.create_or_update(resource_group_name=RESOURCE_GROUP, public_ip_address_name=PUBLIC_IP_ADDRESS_NAME, parameters=BODY)
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
# /PublicIPAddresses/get/GetVMSSPublicIP[get]
#--------------------------------------------------------------------------
print("GetVMSSPublicIP")
# result = mgmt_client.public_ip_addresses.get_virtual_machine_scale_set_public_ip_address(resource_group_name=RESOURCE_GROUP, virtual_machine_scale_set_name=VIRTUAL_MACHINE_SCALE_SET_NAME, virtualmachine_index=VIRTUALMACHINE_INDEX, network_interface_name=NETWORK_INTERFACE_NAME, ip_configuration_name=IP_CONFIGURATION_NAME, public_ip_address_name=PUBLIC_IP_ADDRESS_NAME)


#--------------------------------------------------------------------------
# /PublicIPAddresses/get/ListVMSSVMPublicIP[get]
#--------------------------------------------------------------------------
print("ListVMSSVMPublicIP")
# result = mgmt_client.public_ip_addresses.list_virtual_machine_scale_set_vmpublic_ip_addresses(resource_group_name=RESOURCE_GROUP, virtual_machine_scale_set_name=VIRTUAL_MACHINE_SCALE_SET_NAME, virtualmachine_index=VIRTUALMACHINE_INDEX, network_interface_name=NETWORK_INTERFACE_NAME, ip_configuration_name=IP_CONFIGURATION_NAME)


#--------------------------------------------------------------------------
# /PublicIPAddresses/get/ListVMSSPublicIP[get]
#--------------------------------------------------------------------------
print("ListVMSSPublicIP")
# result = mgmt_client.public_ip_addresses.list_virtual_machine_scale_set_public_ip_addresses(resource_group_name=RESOURCE_GROUP, virtual_machine_scale_set_name=VIRTUAL_MACHINE_SCALE_SET_NAME)


#--------------------------------------------------------------------------
# /PublicIPAddresses/get/Get public IP address[get]
#--------------------------------------------------------------------------
print("Get public IP address")
result = mgmt_client.public_ip_addresses.get(resource_group_name=RESOURCE_GROUP, public_ip_address_name=PUBLIC_IP_ADDRESS_NAME)


#--------------------------------------------------------------------------
# /PublicIPAddresses/get/List resource group public IP addresses[get]
#--------------------------------------------------------------------------
print("List resource group public IP addresses")
result = mgmt_client.public_ip_addresses.list(resource_group_name=RESOURCE_GROUP)


#--------------------------------------------------------------------------
# /PublicIPAddresses/get/List all public IP addresses[get]
#--------------------------------------------------------------------------
print("List all public IP addresses")
result = mgmt_client.public_ip_addresses.list_all()


#--------------------------------------------------------------------------
# /PublicIPAddresses/patch/Update public IP address tags[patch]
#--------------------------------------------------------------------------
print("Update public IP address tags")
TAGS = {
  "tag1": "value1",
  "tag2": "value2"
}
result = mgmt_client.public_ip_addresses.update_tags(resource_group_name=RESOURCE_GROUP, public_ip_address_name=PUBLIC_IP_ADDRESS_NAME, tags=TAGS)


#--------------------------------------------------------------------------
# /PublicIPAddresses/delete/Delete public IP address[delete]
#--------------------------------------------------------------------------
print("Delete public IP address")
result = mgmt_client.public_ip_addresses.delete(resource_group_name=RESOURCE_GROUP, public_ip_address_name=PUBLIC_IP_ADDRESS_NAME)
result = result.result()
