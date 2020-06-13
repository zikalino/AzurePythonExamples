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
POLICY_NAME = "myPolicy"


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
# /WebApplicationFirewallPolicies/put/Creates or updates a WAF policy within a resource group[put]
#--------------------------------------------------------------------------
print("Creates or updates a WAF policy within a resource group")
BODY = {
  "location": AZURE_LOCATION,
  "managed_rules": {
    "managed_rule_sets": [
      {
        "rule_set_type": "OWASP",
        "rule_set_version": "3.0"
      }
    ]
  },
  "custom_rules": [
    {
      "name": "Rule1",
      "priority": "1",
      "rule_type": "MatchRule",
      "action": "Block",
      "match_conditions": [
        {
          "match_variables": [
            {
              "variable_name": "RemoteAddr"
            }
          ],
          "operator": "IPMatch",
          "match_values": [
            "192.168.1.0/24",
            "10.0.0.0/24"
          ]
        }
      ]
    },
    {
      "name": "Rule2",
      "priority": "2",
      "rule_type": "MatchRule",
      "match_conditions": [
        {
          "match_variables": [
            {
              "variable_name": "RemoteAddr"
            }
          ],
          "operator": "IPMatch",
          "match_values": [
            "192.168.1.0/24"
          ]
        },
        {
          "match_variables": [
            {
              "variable_name": "RequestHeaders",
              "selector": "UserAgent"
            }
          ],
          "operator": "Contains",
          "match_values": [
            "Windows"
          ]
        }
      ],
      "action": "Block"
    }
  ]
}
result = mgmt_client.web_application_firewall_policies.create_or_update(resource_group_name=RESOURCE_GROUP, policy_name=POLICY_NAME, parameters=BODY)


#--------------------------------------------------------------------------
# /WebApplicationFirewallPolicies/get/Gets a WAF policy within a resource group[get]
#--------------------------------------------------------------------------
print("Gets a WAF policy within a resource group")
result = mgmt_client.web_application_firewall_policies.get(resource_group_name=RESOURCE_GROUP, policy_name=POLICY_NAME)


#--------------------------------------------------------------------------
# /WebApplicationFirewallPolicies/get/Lists all WAF policies in a resource group[get]
#--------------------------------------------------------------------------
print("Lists all WAF policies in a resource group")
result = mgmt_client.web_application_firewall_policies.list(resource_group_name=RESOURCE_GROUP)


#--------------------------------------------------------------------------
# /WebApplicationFirewallPolicies/get/Lists all WAF policies in a subscription[get]
#--------------------------------------------------------------------------
print("Lists all WAF policies in a subscription")
result = mgmt_client.web_application_firewall_policies.list_all()


#--------------------------------------------------------------------------
# /WebApplicationFirewallPolicies/delete/Deletes a WAF policy within a resource group[delete]
#--------------------------------------------------------------------------
print("Deletes a WAF policy within a resource group")
result = mgmt_client.web_application_firewall_policies.delete(resource_group_name=RESOURCE_GROUP, policy_name=POLICY_NAME)
result = result.result()
