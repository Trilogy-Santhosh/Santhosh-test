#!/usr/bin/env python3
"""
🚀 TRULY AUTOMATED KAYAKO MONITOR - Using MCP Server Directly!

This script calls the Kayako MCP server directly, which:
1. Already has OAuth authentication set up
2. Provides tools to fetch tickets
3. Can be called via HTTP/SSE

We'll use the MCP protocol to fetch tickets programmatically!
"""

import os
import requests
import json
import time
import logging
from datetime import datetime
from typing import List, Dict

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/Users/santhosh.m/Documents/GitHub/Santhosh-test/KayakoNotify/mcp_direct_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
MCP_BASE_URL = "https://mcp.csaiautomations.com/kayako-oauth"
MCP_TOKEN = os.getenv('KAYAKO_MCP_TOKEN')
FLASK_URL = "http://localhost:8080"
CHECK_INTERVAL = 60
USER_ID = "60512164"

# Dashboard criteria
DASHBOARDS = {
    139: {
        "name": "Khoros Classic Community",
        "product_tags": ["khoros_classic"],
        "form_ids": [257],
        "status": "Open"
    },
    143: {
        "name": "Khoros Aurora",
        "product_tags": ["khoros_aurora"],
        "form_ids": [258],
        "status": "Open"
    }
}

seen_tickets = set()


class MCPClient:
    """Client to call MCP tools directly."""
    
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.token = token
        self.session = requests.Session()
        
        if token:
            self.session.headers['Authorization'] = f'Bearer {token}'
            logger.info("✅ MCP client initialized with token")
        else:
            logger.warning("⚠️  No MCP token found in KAYAKO_MCP_TOKEN env var")
    
    def call_tool(self, tool_name: str, arguments: dict) -> dict:
        """
        Call an MCP tool.
        
        Args:
            tool_name: Name of the tool (e.g., 'get_user_tickets')
            arguments: Tool arguments as dict
            
        Returns:
            Tool result as dict
        """
        try:
            # MCP protocol endpoint
            url = f"{self.base_url}/tools/call"
            
            payload = {
                "tool": tool_name,
                "arguments": arguments
            }
            
            logger.debug(f"📞 Calling MCP tool: {tool_name}")
            
            response = self.session.post(url, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return result
            
        except Exception as e:
            logger.error(f"❌ MCP tool call failed: {e}")
            return {}
    
    def get_user_tickets(self, user_id: str) -> List[dict]:
        """Get all tickets for a user."""
        result = self.call_tool('get_user_tickets', {'user_id': user_id})
        return result.get('tickets', [])
    
    def fetch_ticket_details(self, ticket_id: str) -> dict:
        """Fetch full details for a ticket."""
        result = self.call_tool('fetch_ticket_details', {'ticket_id': ticket_id})
        return result.get('ticket', {})


def matches_criteria(ticket: dict, criteria: dict) -> bool:
    """Check if ticket matches dashboard criteria."""
    status = ticket.get('status', '')
    if status != criteria['status']:
        return False
    
    product_tag = ticket.get('product', {}).get('product_tag', '')
    form_id = ticket.get('form', {}).get('id')
    
    return (product_tag in criteria['product_tags'] or 
            form_id in criteria['form_ids'])


def format_for_flask(ticket: dict, dashboard_id: int) -> dict:
    """Format ticket for Flask."""
    return {
        'case_id': ticket.get('id'),
        'subject': ticket.get('subject', 'No Subject'),
        'status': ticket.get('status', 'Unknown'),
        'priority': ticket.get('priority', 'Normal'),
        'requester': ticket.get('requester', {}).get('name', 'Unknown'),
        'requester_email': ticket.get('requester', {}).get('email', ''),
        'assigned_team': ticket.get('assigned_team', {}).get('id', 'Unknown'),
        'created_at': ticket.get('created_at', ''),
        'updated_at': ticket.get('updated_at', ''),
        'product': ticket.get('product', {}).get('product_name', 'Unknown'),
        'product_tag': ticket.get('product', {}).get('product_tag', ''),
        'form_id': ticket.get('form', {}).get('id'),
        'url': f"https://central-supportdesk.kayako.com/agent/conversations/view/{ticket.get('id')}",
        'dashboard_id': dashboard_id
    }


def push_to_flask(dashboard_id: int, cases: List[dict]) -> bool:
    """Push cases to Flask."""
    try:
        url = f"{FLASK_URL}/api/mcp/fetch"
        response = requests.post(url, json={
            "dashboard_id": dashboard_id,
            "cases": cases
        }, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        logger.info(f"✅ Pushed {len(cases)} cases: new={result.get('new')}")
        return True
    except Exception as e:
        logger.error(f"❌ Push failed: {e}")
        return False


def monitoring_cycle(mcp_client: MCPClient):
    """Run one monitoring cycle."""
    logger.info("=" * 80)
    logger.info(f"🔍 CYCLE: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 80)
    
    # Get all user tickets
    tickets = mcp_client.get_user_tickets(USER_ID)
    logger.info(f"📊 Found {len(tickets)} tickets")
    
    # Filter and categorize
    dashboard_cases = {139: [], 143: []}
    
    for ticket_summary in tickets:
        ticket_id = list(ticket_summary.keys())[0]
        status = ticket_summary[ticket_id]
        
        # Only process Open tickets
        if status.lower() != 'open':
            continue
        
        # Fetch full details
        ticket = mcp_client.fetch_ticket_details(ticket_id)
        if not ticket:
            continue
        
        # Check dashboards
        for dashboard_id, criteria in DASHBOARDS.items():
            if matches_criteria(ticket, criteria):
                logger.info(f"  ✅ #{ticket_id} matches Dashboard {dashboard_id}")
                
                case = format_for_flask(ticket, dashboard_id)
                dashboard_cases[dashboard_id].append(case)
                
                if int(ticket_id) not in seen_tickets:
                    logger.info(f"  🆕 NEW CASE!")
                    seen_tickets.add(int(ticket_id))
                
                break
    
    # Push to Flask
    for dashboard_id, cases in dashboard_cases.items():
        if cases:
            logger.info(f"\n📋 Dashboard {dashboard_id}: {len(cases)} cases")
            push_to_flask(dashboard_id, cases)
    
    logger.info("\n")


def main():
    """Main loop."""
    logger.info("🚀" * 40)
    logger.info("🚀 MCP DIRECT MONITOR - STARTING")
    logger.info("🚀" * 40)
    logger.info(f"   MCP Server: {MCP_BASE_URL}")
    logger.info(f"   Flask URL: {FLASK_URL}")
    logger.info(f"   Interval: {CHECK_INTERVAL}s")
    logger.info("=" * 80 + "\n")
    
    # Check for MCP token
    if not MCP_TOKEN:
        logger.error("❌ KAYAKO_MCP_TOKEN environment variable not set!")
        logger.error("   Get token from: https://mcp.csaiautomations.com")
        return
    
    # Initialize MCP client
    mcp_client = MCPClient(MCP_BASE_URL, MCP_TOKEN)
    
    # Check Flask
    try:
        response = requests.get(f"{FLASK_URL}/api/status", timeout=5)
        logger.info(f"✅ Flask running: {response.json()}\n")
    except Exception as e:
        logger.error(f"❌ Flask not accessible: {e}\n")
        return
    
    # Main loop
    cycle = 0
    while True:
        try:
            cycle += 1
            logger.info(f"🔄 Cycle #{cycle}")
            
            monitoring_cycle(mcp_client)
            
            logger.info(f"💤 Sleeping {CHECK_INTERVAL}s...\n")
            time.sleep(CHECK_INTERVAL)
            
        except KeyboardInterrupt:
            logger.info("\n⛔ Stopped")
            break
        except Exception as e:
            logger.error(f"❌ Error: {e}", exc_info=True)
            time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()



