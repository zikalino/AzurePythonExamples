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
INBOUND_NAT_POOL_NAME = "myInboundNatPool"
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
  "sku": {
    "name": "Standard"
  },
  "public_ip_allocation_method": "Static",
  "location": AZURE_LOCATION
}
result = mgmt_client.public_ip_addresses.create_or_update(resource_group_name=RESOURCE_GROUP, public_ip_address_name=PUBLIC_IP_ADDRESS_NAME, parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /LoadBalancers/put/Create load balancer with Frontend IP in Zone 1[put]
#--------------------------------------------------------------------------
print("Create load balancer with Frontend IP in Zone 1")
BODY = {
  "location": AZURE_LOCATION,
  "sku": {
    "name": "Standard"
  },
  "frontend_ip_configurations": [
    {
      "name": FRONTEND_IP_CONFIGURATION_NAME,
      "zones": [
        "1"
      ],
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
      "protocol": "Tcp"
    }
  ],
  "inbound_nat_pools": [],
  "outbound_rules": []
}
result = mgmt_client.load_balancers.create_or_update(resource_group_name=RESOURCE_GROUP, load_balancer_name=LOAD_BALANCER_NAME, parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /LoadBalancers/put/Create load balancer with outbound rules[put]
#--------------------------------------------------------------------------
print("Create load balancer with outbound rules")
BODY = {
  "location": AZURE_LOCATION,
  "sku": {
    "name": "Standard"
  },
  "frontend_ip_configurations": [
    {
      "name": FRONTEND_IP_CONFIGURATION_NAME,
      "public_ip_address": {
        "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/publicIPAddresses/" + PUBLIC_IP_ADDRESS_NAME
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
      "backend_address_pool": {
        "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/loadBalancers/" + LOAD_BALANCER_NAME + "/backendAddressPools/" + BACKEND_ADDRESS_POOL_NAME
      },
      "probe": {
        "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/loadBalancers/" + LOAD_BALANCER_NAME + "/probes/" + PROBE_NAME
      },
      "protocol": "Tcp",
      "load_distribution": "Default",
      "frontend_port": "80",
      "backend_port": "80",
      "idle_timeout_in_minutes": "15",
      "enable_floating_ip": True,
      "disable_outbound_snat": True
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
      "protocol": "Tcp"
    }
  ],
  "inbound_nat_pools": [],
  "outbound_rules": [
    {
      "name": "rule1",
      "backend_address_pool": {
        "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/loadBalancers/" + LOAD_BALANCER_NAME + "/backendAddressPools/" + BACKEND_ADDRESS_POOL_NAME
      },
      "frontend_ip_configurations": [
        {
          "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/loadBalancers/" + LOAD_BALANCER_NAME + "/frontendIPConfigurations/" + FRONTEND_IP_CONFIGURATION_NAME
        }
      ],
      "protocol": "All"
    }
  ]
}
result = mgmt_client.load_balancers.create_or_update(resource_group_name=RESOURCE_GROUP, load_balancer_name=LOAD_BALANCER_NAME, parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /LoadBalancers/put/Create load balancer with Standard SKU[put]
#--------------------------------------------------------------------------
print("Create load balancer with Standard SKU")
BODY = {
  "location": AZURE_LOCATION,
  "sku": {
    "name": "Standard"
  },
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
      "protocol": "Tcp"
    }
  ],
  "inbound_nat_pools": [],
  "outbound_rules": []
}
result = mgmt_client.load_balancers.create_or_update(resource_group_name=RESOURCE_GROUP, load_balancer_name=LOAD_BALANCER_NAME, parameters=BODY)
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
# /LoadBalancers/put/Create load balancer with inbound nat pool[put]
#--------------------------------------------------------------------------
print("Create load balancer with inbound nat pool")
BODY = {
  "location": AZURE_LOCATION,
  "sku": {
    "name": "Standard"
  },
  "frontend_ip_configurations": [
    {
      "name": FRONTEND_IP_CONFIGURATION_NAME,
      "zones": [],
      "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/loadBalancers/" + LOAD_BALANCER_NAME + "/frontendIPConfigurations/" + FRONTEND_IP_CONFIGURATION_NAME,
      "private_ipallocation_method": "Dynamic",
      "subnet": {
        "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualNetworks/" + VIRTUAL_NETWORK_NAME + "/subnets/" + SUBNET_NAME
      }
    }
  ],
  "backend_address_pools": [],
  "load_balancing_rules": [],
  "probes": [],
  "inbound_nat_rules": [],
  "outbound_rules": [],
  "inbound_nat_pools": [
    {
      "name": "test",
      "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/loadBalancers/" + LOAD_BALANCER_NAME + "/inboundNatPools/" + INBOUND_NAT_POOL_NAME,
      "frontend_ip_configuration": {
        "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/loadBalancers/" + LOAD_BALANCER_NAME + "/frontendIPConfigurations/" + FRONTEND_IP_CONFIGURATION_NAME
      },
      "protocol": "Tcp",
      "frontend_port_range_start": "8080",
      "frontend_port_range_end": "8085",
      "backend_port": "8888",
      "idle_timeout_in_minutes": "10",
      "enable_floating_ip": True,
      "enable_tcp_reset": True
    }
  ]
}
result = mgmt_client.load_balancers.create_or_update(resource_group_name=RESOURCE_GROUP, load_balancer_name=LOAD_BALANCER_NAME, parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /LoadBalancers/get/Get load balancer[get]
#--------------------------------------------------------------------------
print("Get load balancer")
result = mgmt_client.load_balancers.get(resource_group_name=RESOURCE_GROUP, load_balancer_name=LOAD_BALANCER_NAME)


#--------------------------------------------------------------------------
# /LoadBalancers/get/List load balancers in resource group[get]
#--------------------------------------------------------------------------
print("List load balancers in resource group")
result = mgmt_client.load_balancers.list(resource_group_name=RESOURCE_GROUP)


#--------------------------------------------------------------------------
# /LoadBalancers/get/List all load balancers[get]
#--------------------------------------------------------------------------
print("List all load balancers")
result = mgmt_client.load_balancers.list_all()


#--------------------------------------------------------------------------
# /LoadBalancers/patch/Update load balancer tags[patch]
#--------------------------------------------------------------------------
print("Update load balancer tags")
TAGS = {
  "tag1": "value1",
  "tag2": "value2"
}
result = mgmt_client.load_balancers.update_tags(resource_group_name=RESOURCE_GROUP, load_balancer_name=LOAD_BALANCER_NAME, tags=TAGS)


#--------------------------------------------------------------------------
# /LoadBalancers/delete/Delete load balancer[delete]
#--------------------------------------------------------------------------
print("Delete load balancer")
result = mgmt_client.load_balancers.delete(resource_group_name=RESOURCE_GROUP, load_balancer_name=LOAD_BALANCER_NAME)
result = result.result()
