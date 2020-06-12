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
FIREWALL_POLICY_NAME = "myFirewallPolicy"
RULE_GROUP_NAME = "myRuleGroup"


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
# /FirewallPolicies/put/Create FirewallPolicy[put]
#--------------------------------------------------------------------------
print("Create FirewallPolicy")
BODY = {
  "tags": {
    "key1": "value1"
  },
  "location": AZURE_LOCATION,
  "threat_intel_mode": "Alert",
  "threat_intel_whitelist": {
    "ip_addresses": [
      "20.3.4.5"
    ],
    "fqdns": [
      "*.microsoft.com"
    ]
  }
}
result = mgmt_client.firewall_policies.create_or_update(resource_group_name=RESOURCE_GROUP, firewall_policy_name=FIREWALL_POLICY_NAME, parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /FirewallPolicyRuleGroups/put/Create FirewallPolicyRuleGroup[put]
#--------------------------------------------------------------------------
print("Create FirewallPolicyRuleGroup")
BODY = {
  "priority": "110",
  "rules": [
    {
      "rule_type": "FirewallPolicyFilterRule",
      "name": "Example-Filter-Rule",
      "action": {
        "type": "Deny"
      },
      "rule_conditions": [
        {
          "rule_condition_type": "NetworkRuleCondition",
          "name": "network-condition1",
          "source_addresses": [
            "10.1.25.0/24"
          ],
          "destination_addresses": [
            "*"
          ],
          "ip_protocols": [
            "TCP"
          ],
          "destination_ports": [
            "*"
          ]
        }
      ]
    }
  ]
}
result = mgmt_client.firewall_policy_rule_groups.create_or_update(resource_group_name=RESOURCE_GROUP, firewall_policy_name=FIREWALL_POLICY_NAME, rule_group_name=RULE_GROUP_NAME, parameters=BODY)
result = result.result()


#--------------------------------------------------------------------------
# /FirewallPolicyRuleGroups/put/Create FirewallPolicyRuleGroup With IpGroups[put]
#--------------------------------------------------------------------------
print("Create FirewallPolicyRuleGroup With IpGroups")
BODY = {
  "priority": "110",
  "rules": [
    {
      "rule_type": "FirewallPolicyFilterRule",
      "name": "Example-Filter-Rule",
      "action": {
        "type": "Deny"
      },
      "rule_conditions": [
        {
          "rule_condition_type": "NetworkRuleCondition",
          "name": "network-condition1",
          "ip_protocols": [
            "TCP"
          ],
          "destination_ports": [
            "*"
          ],
          "source_ip_groups": [
            "/subscriptions/subid/providers/Microsoft.Network/resourceGroup/rg1/ipGroups/ipGroups1"
          ],
          "destination_ip_groups": [
            "/subscriptions/subid/providers/Microsoft.Network/resourceGroup/rg1/ipGroups/ipGroups2"
          ]
        }
      ]
    }
  ]
}
#result = mgmt_client.firewall_policy_rule_groups.create_or_update(resource_group_name=RESOURCE_GROUP, firewall_policy_name=FIREWALL_POLICY_NAME, rule_group_name=RULE_GROUP_NAME, parameters=BODY)
#result = result.result()


#--------------------------------------------------------------------------
# /FirewallPolicyRuleGroups/get/Get FirewallPolicyRuleGroup With IpGroups[get]
#--------------------------------------------------------------------------
print("Get FirewallPolicyRuleGroup With IpGroups")
result = mgmt_client.firewall_policy_rule_groups.get(resource_group_name=RESOURCE_GROUP, firewall_policy_name=FIREWALL_POLICY_NAME, rule_group_name=RULE_GROUP_NAME)


#--------------------------------------------------------------------------
# /FirewallPolicyRuleGroups/get/Get FirewallPolicyRuleGroup[get]
#--------------------------------------------------------------------------
print("Get FirewallPolicyRuleGroup")
result = mgmt_client.firewall_policy_rule_groups.get(resource_group_name=RESOURCE_GROUP, firewall_policy_name=FIREWALL_POLICY_NAME, rule_group_name=RULE_GROUP_NAME)


#--------------------------------------------------------------------------
# /FirewallPolicyRuleGroups/get/List all FirewallPolicyRuleGroups for a given FirewallPolicy[get]
#--------------------------------------------------------------------------
print("List all FirewallPolicyRuleGroups for a given FirewallPolicy")
result = mgmt_client.firewall_policy_rule_groups.list(resource_group_name=RESOURCE_GROUP, firewall_policy_name=FIREWALL_POLICY_NAME)


#--------------------------------------------------------------------------
# /FirewallPolicyRuleGroups/get/List all FirewallPolicyRuleGroups with IpGroups for a given FirewallPolicy[get]
#--------------------------------------------------------------------------
print("List all FirewallPolicyRuleGroups with IpGroups for a given FirewallPolicy")
result = mgmt_client.firewall_policy_rule_groups.list(resource_group_name=RESOURCE_GROUP, firewall_policy_name=FIREWALL_POLICY_NAME)


#--------------------------------------------------------------------------
# /FirewallPolicies/get/Get FirewallPolicy[get]
#--------------------------------------------------------------------------
print("Get FirewallPolicy")
result = mgmt_client.firewall_policies.get(resource_group_name=RESOURCE_GROUP, firewall_policy_name=FIREWALL_POLICY_NAME)


#--------------------------------------------------------------------------
# /FirewallPolicies/get/List all Firewall Policies for a given resource group[get]
#--------------------------------------------------------------------------
print("List all Firewall Policies for a given resource group")
result = mgmt_client.firewall_policies.list(resource_group_name=RESOURCE_GROUP)


#--------------------------------------------------------------------------
# /FirewallPolicies/get/List all Firewall Policies for a given subscription[get]
#--------------------------------------------------------------------------
print("List all Firewall Policies for a given subscription")
result = mgmt_client.firewall_policies.list_all()


#--------------------------------------------------------------------------
# /FirewallPolicyRuleGroups/delete/Delete FirewallPolicyRuleGroup[delete]
#--------------------------------------------------------------------------
print("Delete FirewallPolicyRuleGroup")
result = mgmt_client.firewall_policy_rule_groups.delete(resource_group_name=RESOURCE_GROUP, firewall_policy_name=FIREWALL_POLICY_NAME, rule_group_name=RULE_GROUP_NAME)
result = result.result()


#--------------------------------------------------------------------------
# /FirewallPolicies/delete/Delete Firewall Policy[delete]
#--------------------------------------------------------------------------
print("Delete Firewall Policy")
result = mgmt_client.firewall_policies.delete(resource_group_name=RESOURCE_GROUP, firewall_policy_name=FIREWALL_POLICY_NAME)
result = result.result()
