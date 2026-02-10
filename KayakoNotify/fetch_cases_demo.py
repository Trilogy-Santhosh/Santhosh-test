#!/usr/bin/env python3
"""
Live Demo: Fetch Kayako Cases Using MCP

This script demonstrates EXACTLY how to use the Kayako MCP to fetch ticket details.

USAGE:
    python3 fetch_cases_demo.py

Note: This shows the concept. Actual MCP calls require running in Cursor environment
or having an MCP API bridge set up.
"""

import json
from datetime import datetime

# Sample case IDs from your dashboards
# Replace these with actual case IDs from your dashboards
SAMPLE_CASES = {
    139: [  # Khoros Classic Community dashboard
        # Add case IDs from Dashboard 139 here
        # Example: 60144273, 60144274, ...
    ],
    143: [  # Khoros Aurora dashboard
        60144273,  # Spanish login loop issue we looked at earlier
        # Add more case IDs from Dashboard 143 here
    ]
}


def demo_fetch_single_ticket():
    """
    Demonstrates fetching a single ticket via MCP.
    
    In Cursor, you would simply ask:
    "Fetch details of Kayako ticket 60144273 using MCP"
    
    Or call the tool directly:
    mcp_kayako-oauth_fetch_ticket_details(ticket_id="60144273")
    """
    
    print("\n" + "="*70)
    print("DEMO 1: Fetch Single Ticket")
    print("="*70)
    
    ticket_id = "60144273"
    
    print(f"\n📋 Fetching ticket #{ticket_id}...")
    print("\nMCP Call:")
    print(f"  Tool: mcp_kayako-oauth_fetch_ticket_details")
    print(f"  Params: ticket_id='{ticket_id}'")
    
    print("\n✅ What you'd get back:")
    print("""
    {
      "id": 60144273,
      "subject": "[00443499] Spanish version of site login loop",
      "status": "Hold",
      "priority": "High",
      "requester": {
        "name": "Heaven McCullough",
        "email": "heaven.stephenson6@t-mobile.com",
        "organizationId": 60067484
      },
      "assigned_team": {"id": 4},
      "assigned_agent": {...},
      "product": {
        "product_name": "Khoros Community Aurora",
        "business_unit": "Khoros"
      },
      "jira_link": "KPSSUPPORT-55",
      "post_count": 44,
      "has_attachments": true,
      "has_notes": true,
      "created_at": "2025-02-07T00:10:44+00:00",
      "updated_at": "2025-12-25T12:30:48+00:00",
      "translog": {
        "2025-12-25T12:30:47+00:00": "PS team still investigating...",
        // Complete history of all updates
      }
    }
    """)


def demo_fetch_organization_tickets():
    """
    Demonstrates fetching all tickets for an organization.
    """
    
    print("\n" + "="*70)
    print("DEMO 2: Fetch All Tickets for an Organization")
    print("="*70)
    
    org_id = "60067484"  # T-Mobile's org ID from the ticket above
    
    print(f"\n🏢 Fetching all tickets for organization #{org_id}...")
    print("\nMCP Call:")
    print(f"  Tool: mcp_kayako-oauth_get_organization_tickets")
    print(f"  Params: organization_id='{org_id}'")
    
    print("\n✅ This returns ALL tickets for T-Mobile USA, Inc.")
    print("   You could then filter by status, priority, product, etc.")


def demo_workflow_for_dashboard_monitoring():
    """
    Shows the complete workflow for your dashboard monitor.
    """
    
    print("\n" + "="*70)
    print("DEMO 3: Complete Workflow for Dashboard Monitoring")
    print("="*70)
    
    print("\n📊 Monitoring Dashboard 143 (Khoros Aurora)")
    print("\n" + "-"*70)
    print("STEP 1: Get Case IDs from Dashboard (Selenium)")
    print("-"*70)
    
    # Simulating what Selenium would return
    dashboard_cases = [60144273, 60144274, 60144275]  # Example IDs
    print(f"  ✓ Selenium found {len(dashboard_cases)} cases")
    print(f"  ✓ Case IDs: {dashboard_cases}")
    
    print("\n" + "-"*70)
    print("STEP 2: Enrich Each Case with MCP")
    print("-"*70)
    
    for case_id in dashboard_cases[:2]:  # Show first 2 as examples
        print(f"\n  📋 Case #{case_id}")
        print(f"     MCP Call: fetch_ticket_details('{case_id}')")
        print(f"     Returns: Full details with history, Jira links, etc.")
    
    print("\n" + "-"*70)
    print("STEP 3: Check for New Cases & Notify")
    print("-"*70)
    
    print("""
  For each enriched case:
    1. Check if case_id is in seen_cases database
    2. If new:
       - Send desktop notification with rich details
       - Save to database
       - Optional: Find similar past tickets
       - Optional: Lookup organization in NetSuite/Salesforce
    """)


def demo_advanced_features():
    """
    Shows advanced features you get with MCP.
    """
    
    print("\n" + "="*70)
    print("DEMO 4: Advanced MCP Features")
    print("="*70)
    
    ticket_id = "60144273"
    
    print("\n1️⃣ Find Similar Tickets (Semantic Search)")
    print(f"   MCP Call: get_similar_tickets(ticket_id='{ticket_id}')")
    print("   Use Case: 'Has this issue happened before?'")
    
    print("\n2️⃣ Add Internal Note")
    print(f"   MCP Call: add_internal_note(")
    print(f"     ticket_id='{ticket_id}',")
    print(f"     note='Escalated to PS team - investigating Spanish SSO'")
    print(f"   )")
    print("   Use Case: Auto-add notes when escalating")
    
    print("\n3️⃣ Get Customer Info from CRM")
    print("   MCP Call: search_organization_both('T-Mobile')")
    print("   Returns: NetSuite + Salesforce data side-by-side")
    print("   Use Case: 'Is this customer Platinum? What's their ARR?'")
    
    print("\n4️⃣ Apply Macro")
    print("   MCP Call: send_to_external_team_macro(")
    print(f"     ticket_id='{ticket_id}',")
    print("     external_team='Engineering',")
    print("     key='KPSSUPPORT-55',")
    print("     offset=24")
    print("   )")
    print("   Use Case: Auto-escalate critical issues")


def demo_practical_integration():
    """
    Shows practical integration code you could use.
    """
    
    print("\n" + "="*70)
    print("DEMO 5: Practical Integration Code")
    print("="*70)
    
    code = '''
# In your KayakoNotify app, add this:

class MCPEnhancedMonitor:
    def fetch_and_enrich_cases(self, dashboard_id):
        """Fetch cases with MCP enrichment."""
        
        # Step 1: Selenium scraping (your existing code)
        case_ids = self._scrape_dashboard(dashboard_id)
        
        # Step 2: Enrich with MCP
        enriched_cases = []
        for case_id in case_ids:
            # Call MCP via Cursor AI
            case_data = self._fetch_via_mcp(case_id)
            
            if case_data:
                # Extract rich details
                case = EnhancedCase(
                    id=case_data['id'],
                    subject=case_data['subject'],
                    status=case_data['status'],
                    priority=case_data.get('priority'),
                    requester_email=case_data['requester']['email'],
                    organization=case_data.get('organization'),
                    product=case_data.get('product', {}).get('product_name'),
                    jira_link=case_data.get('jira_link'),
                    post_count=case_data.get('post_count', 0),
                    has_attachments=case_data.get('has_attachments', False)
                )
                
                enriched_cases.append(case)
        
        return enriched_cases
    
    def _fetch_via_mcp(self, ticket_id):
        """
        Call MCP tool to fetch ticket details.
        
        In Cursor: Direct tool call
        Standalone: Need MCP API bridge
        """
        # This is where you'd call the MCP tool
        # Implementation depends on your environment
        pass
'''
    
    print(code)


def show_next_steps():
    """
    Shows what to do next.
    """
    
    print("\n" + "="*70)
    print("🚀 NEXT STEPS")
    print("="*70)
    
    print("""
1. ✅ TEST IN CURSOR (Easiest!)
   - Open Cursor AI chat
   - Ask: "Fetch details of Kayako ticket 60144273 using MCP"
   - See the rich data you'd get

2. 📋 GET YOUR CASE IDS
   - Run your current monitor with Selenium
   - Note down some case IDs from Dashboard 139 and 143
   - Test fetching them via MCP in Cursor

3. 🔗 INTEGRATE (When Ready)
   - Add MCP client to your app.py
   - Call MCP after Selenium gets case IDs
   - Enhance notifications with rich data

4. 🎁 ADD ADVANCED FEATURES (Optional)
   - Similar ticket finder
   - CRM data lookup
   - Auto-escalation with macros
   - Auto-note adding

📚 Read MCP_INTEGRATION_GUIDE.md for full details!
""")


def main():
    """
    Run all demos.
    """
    
    print("\n" + "="*70)
    print("🔔 KAYAKO MCP - LIVE DEMO")
    print("="*70)
    print("\nThis demonstrates how to use the Kayako OAuth MCP")
    print("to fetch ticket details for your dashboard monitor.")
    print("\nNote: MCP calls shown are conceptual.")
    print("To actually run them, use Cursor AI or set up an MCP bridge.")
    print("="*70)
    
    # Run all demos
    demo_fetch_single_ticket()
    demo_fetch_organization_tickets()
    demo_workflow_for_dashboard_monitoring()
    demo_advanced_features()
    demo_practical_integration()
    show_next_steps()
    
    print("\n" + "="*70)
    print("✨ Demo Complete!")
    print("="*70)
    print("\n💡 TIP: Try this in Cursor AI right now:")
    print('   "Fetch details of Kayako ticket 60144273 using MCP"')
    print("\n📖 See MCP_SUMMARY.md for a quick overview")
    print("📖 See MCP_INTEGRATION_GUIDE.md for full documentation")
    print("\n")


if __name__ == '__main__':
    main()



