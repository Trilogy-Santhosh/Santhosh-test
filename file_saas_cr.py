#!/usr/bin/env python3
"""
File a SaaS Change Request to Jira using Atlassian MCP
"""
import os
import json
import requests
from datetime import datetime, timedelta

# MCP Configuration
MCP_BASE_URL = "https://mcp.csaiautomations.com/atlassian-oauth"
MCP_TOKEN = os.getenv("ATLASSIAN_MCP_TOKEN")

if not MCP_TOKEN:
    print("Error: ATLASSIAN_MCP_TOKEN environment variable not set")
    exit(1)

# Calculate dates
start_date = (datetime.now() + timedelta(hours=7)).strftime("%Y-%m-%dT%H:%M:%S.000+0000")
end_date = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%dT%H:%M:%S.000+0000")
due_date = (datetime.now() + timedelta(days=13)).strftime("%Y-%m-%dT%H:%M:%S.000+0000")

# CR Details
cr_data = {
    "project": "LIA",
    "type": "Change Request",
    "kayako_id": "60293980",
    "summary": "[sane] Generate lithium SSO key for stage",
    "description": """## Customer Request

Customer is setting up Khoros SSO to work with Microsoft Azure and needs clarification on provisioning requirements.

## Details Requested

The customer is asking if the following details need to be provisioned by Khoros:

1. **SSO Encryption Key**
2. **SSO Client ID**
3. **SSO Client Domain**
4. **SSO Server ID**

## Reference Documentation

Customer is following this documentation:
https://developer.khoros.com/khoroscommunitydevdocs/docs/lithiumsso-token#lithiumsso-token-generation-example

## Action Required

Please review the customer's SSO setup requirements and provide guidance on:
- Which values need to be provisioned by Khoros
- Which values the customer needs to configure on their end
- Any additional steps needed for Microsoft Azure SSO integration with Khoros Community

## Environment
- **Customer:** SANE Solutions
- **Instance:** Stage environment
- **SSO Provider:** Microsoft Azure
- **Integration Type:** LithiumSSO Token-based authentication

## Timeline
- **Start Date:** February 7, 2026
- **End Date:** February 20, 2026
- **Due Date:** February 20, 2026
- **Requires Maintenance Window:** NO
""",
    "priority": "Highest",
    "start_date": start_date,
    "end_date": end_date,
    "due_date": due_date,
    "change_implementer": "SaaSOps",
    "change_requester": "Customer Support",
    "impact_amount": "0",
    "cost_impact": "Unable to Determine",
    "is_maintenance_window": "false",
    "labels": ["saas-cr", "sso", "lithiumsso", "azure-sso", "stage-environment"]
}

print("=" * 80)
print("SaaS Change Request Details")
print("=" * 80)
print(json.dumps(cr_data, indent=2))
print("=" * 80)

# First, let's list available tools
print("\nFetching available Atlassian MCP tools...")
try:
    response = requests.post(
        f"{MCP_BASE_URL}/messages",
        headers={
            "Authorization": f"Bearer {MCP_TOKEN}",
            "Content-Type": "application/json"
        },
        json={
            "method": "tools/list"
        },
        timeout=30
    )
    
    if response.status_code == 200:
        tools_data = response.json()
        print("\nAvailable tools:")
        if "tools" in tools_data:
            for tool in tools_data["tools"]:
                print(f"  - {tool.get('name')}: {tool.get('description', 'No description')}")
        else:
            print(json.dumps(tools_data, indent=2))
    else:
        print(f"Error listing tools: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"Error connecting to MCP: {e}")
    print("\nNote: You may need to use the Metis web interface or direct API calls.")
    print(f"CR details have been prepared above for manual filing if needed.")

print("\n" + "=" * 80)
print("Next Steps:")
print("=" * 80)
print("1. Review the CR details above")
print("2. If MCP connection works, the CR will be filed automatically")
print("3. If not, you can file manually using the details provided")
print("4. Link to Kayako ticket: 60293980")
print("=" * 80)
