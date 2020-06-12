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
LOAD_BALANCER_NAME = "myLoadBalancer"
FRONTEND_IP_CONFIGURATION_NAME = "myFrontendIpConfiguration"
VIRTUAL_NETWORK_NAME = "myVirtualNetwork"
SUBNET_NAME = "mySubnet"
BACKEND_ADDRESS_POOL_NAME = "myBackendAddressPoolName"
PROBE_NAME = "myProbe"
INBOUND_NAT_RULE_NAME = "myInboundNatRuleName"
PUBLIC_IP_ADDRESS_NAME = "myPublicIpAddress"


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
# /VirtualNetworks/put/Create virtual network[put]
#--------------------------------------------------------------------------
print("Create virtual network")
BODY = {
  "location": AZURE_LOCATION,
  "address_space": {
    "address_prefixes": [
      "10.0.0.0/16"
    ]
  }
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
# /LoadBalancers/put/Create load balancer[put]
#--------------------------------------------------------------------------
print("Create load balancer")
BODY = {
  "location": AZURE_LOCATION,
  "frontend_ip_configurations": [
    {
      "name": FRONTEND_IP_CONFIGURATION_NAME,
      "subnet": {
        "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualNetworks/" + VIRTUAL_NETWORK_NAME + "/subnets/" + SUBNET_NAME
      }
    }
  ],
  "backend_address_pools": [
    {
      "name": BACKEND_ADDRESS_POOL_NAME
    }
  ],
  "load_balancing_rules": [
    {
      "name": "rulelb",
      "frontend_ip_configuration": {
        "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/loadBalancers/" + LOAD_BALANCER_NAME + "/frontendIPConfigurations/" + FRONTEND_IP_CONFIGURATION_NAME
      },
      "frontend_port": "80",
      "backend_port": "80",
      "enable_floating_ip": True,
      "idle_timeout_in_minutes": "15",
      "protocol": "Tcp",
      "enable_tcp_reset": False,
      "load_distribution": "Default",
      "backend_address_pool": {
        "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/loadBalancers/" + LOAD_BALANCER_NAME + "/backendAddressPools/" + BACKEND_ADDRESS_POOL_NAME
      },
      "probe": {
        "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/loadBalancers/" + LOAD_BALANCER_NAME + "/probes/" + PROBE_NAME
      }
    }
  ],
  "probes": [
    {
      "name": PROBE_NAME,
      "protocol": "Http",
      "port": "80",
      "request_path": "healthcheck.aspx",
      "interval_in_seconds": "15",
      "number_of_probes": "2"
    }
  ],
  "inbound_nat_rules": [
    {
      "name": INBOUND_NAT_RULE_NAME,
      "frontend_ip_configuration": {
        "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/loadBalancers/" + LOAD_BALANCER_NAME + "/frontendIPConfigurations/" + FRONTEND_IP_CONFIGURATION_NAME
      },
      "frontend_port": "3389",
      "backend_port": "3389",
      "enable_floating_ip": True,
      "idle_timeout_in_minutes": "15",
      "protocol": "Tcp",
      "enable_tcp_reset": False
    }
  ],
  "inbound_nat_pools": []
}
result = mgmt_client.load_balancers.create_or_update(resource_group_name=RESOURCE_GROUP, load_balancer_name=LOAD_BALANCER_NAME, parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /InboundNatRules/put/InboundNatRuleCreate[put]
#--------------------------------------------------------------------------
print("InboundNatRuleCreate")
BODY = {
  "protocol": "Tcp",
  "frontend_ip_configuration": {
    "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/loadBalancers/" + LOAD_BALANCER_NAME + "/frontendIPConfigurations/" + FRONTEND_IP_CONFIGURATION_NAME
  },
  "frontend_port": "3390",
  "backend_port": "3389",
  "idle_timeout_in_minutes": "4",
  "enable_tcp_reset": False,
  "enable_floating_ip": False
}
result = mgmt_client.inbound_nat_rules.create_or_update(resource_group_name=RESOURCE_GROUP, load_balancer_name=LOAD_BALANCER_NAME, inbound_nat_rule_name=INBOUND_NAT_RULE_NAME, inbound_nat_rule_parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /InboundNatRules/get/InboundNatRuleGet[get]
#--------------------------------------------------------------------------
print("InboundNatRuleGet")
result = mgmt_client.inbound_nat_rules.get(resource_group_name=RESOURCE_GROUP, load_balancer_name=LOAD_BALANCER_NAME, inbound_nat_rule_name=INBOUND_NAT_RULE_NAME)


#--------------------------------------------------------------------------
# /InboundNatRules/get/InboundNatRuleList[get]
#--------------------------------------------------------------------------
print("InboundNatRuleList")
result = mgmt_client.inbound_nat_rules.list(resource_group_name=RESOURCE_GROUP, load_balancer_name=LOAD_BALANCER_NAME)


#--------------------------------------------------------------------------
# /InboundNatRules/delete/InboundNatRuleDelete[delete]
#--------------------------------------------------------------------------
print("InboundNatRuleDelete")
result = mgmt_client.inbound_nat_rules.delete(resource_group_name=RESOURCE_GROUP, load_balancer_name=LOAD_BALANCER_NAME, inbound_nat_rule_name=INBOUND_NAT_RULE_NAME)
result = result.result()
