# 🔗 Kayako MCP Integration Guide

## Overview

This guide explains how to integrate the **Kayako OAuth MCP** into your dashboard monitoring tool.

## 🎯 What the MCP Provides

The Kayako OAuth MCP gives you access to:

### ✅ Available Operations

1. **Ticket Operations**
   - `fetch_ticket_details` - Get comprehensive ticket info including history
   - `add_internal_note` - Add private notes to tickets
   - `create_ticket` - Create new tickets with auto-resolution of brands/teams

2. **User & Organization**
   - `get_user_organization` - Find organization by user email
   - `get_organization_members` - Get all members of an organization
   - `get_user_tickets` - All tickets for a specific user
   - `get_organization_tickets` - All tickets for an organization
   - `get_customer_by_email` - Find customer by email
   - `get_colleagues` - Find colleagues of a user

3. **Organization Details**
   - `get_organization_details_by_id` - Full org details by ID
   - `get_organization_details_by_name` - Search org by name
   - Includes: support level, ARR, NetSuite ID, Salesforce ID, status, etc.

4. **CRM Integration**
   - `get_netsuite_customer` - NetSuite data by ID/email/company/domain
   - `get_salesforce_account` - Salesforce data by ID/email/company/domain
   - `search_organization_both` - Search both NetSuite and Salesforce simultaneously
   - `get_organization_by_ids` - Get data from both systems using IDs

5. **Advanced Features**
   - `get_similar_tickets` - Semantic search for similar tickets (requires OpenAI)

6. **Macros**
   - `send_to_customer_macro` - Reply to customer and set Pending
   - `send_to_external_team_macro` - Escalate to teams (SaaS Ops, Engineering, etc.)
   - `send_to_qc_macro` - Send for QC review
   - `close_ticket_*_macro` - Various closing workflows

### ❌ Limitations

The MCP **cannot**:
- Query tickets by dashboard ID
- Filter tickets by brand or product
- Search tickets by custom fields
- Access dashboard-specific filtered views

## 🔄 Integration Strategy: Hybrid Approach

### Recommended: Selenium + MCP

**Best of both worlds:**

1. **Selenium** - Scrape dashboards to get case IDs
   - Respects your dashboard filters (brand, status, etc.)
   - Gets the exact list of cases shown in the dashboard

2. **MCP** - Enrich each case with rich details
   - No manual session management
   - Rich data: history, Jira links, org details, product info
   - Advanced features: similar tickets, CRM lookups

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Dashboard Monitor Service                               │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  Step 1: Discover Case IDs                              │
│  ┌────────────────────────────────────┐                 │
│  │  Selenium Web Scraper              │                 │
│  │  - Load dashboard 139, 143         │                 │
│  │  - Extract case IDs from HTML      │                 │
│  │  - Output: [12345, 12346, ...]     │                 │
│  └────────────────────────────────────┘                 │
│                    │                                      │
│                    ▼                                      │
│  Step 2: Enrich with MCP                                │
│  ┌────────────────────────────────────┐                 │
│  │  Kayako MCP Client                 │                 │
│  │  - fetch_ticket_details(12345)     │                 │
│  │  - Returns: Full ticket data       │                 │
│  │    * Subject, status, priority     │                 │
│  │    * Requester + organization      │                 │
│  │    * Product, brand, Jira link     │                 │
│  │    * Full transaction history      │                 │
│  │    * Attachment metadata           │                 │
│  └────────────────────────────────────┘                 │
│                    │                                      │
│                    ▼                                      │
│  Step 3: Notification Logic                             │
│  ┌────────────────────────────────────┐                 │
│  │  - Check if case is new            │                 │
│  │  - Send desktop notification       │                 │
│  │  - Update dashboard UI             │                 │
│  │  - Play sound alert                │                 │
│  └────────────────────────────────────┘                 │
└─────────────────────────────────────────────────────────┘
```

## 💻 Implementation

### Option 1: Direct MCP Integration (In Cursor)

If running within Cursor, you can call MCP tools directly:

```python
class KayakoMCPClient:
    def fetch_ticket_details(self, ticket_id: int):
        """Fetch ticket via MCP."""
        # In Cursor, this would be a direct tool call
        result = call_mcp_tool(
            "mcp_kayako-oauth_fetch_ticket_details",
            {"ticket_id": str(ticket_id)}
        )
        return result
```

### Option 2: MCP via API Bridge (Standalone)

For standalone operation outside Cursor, you'd need an API bridge:

```python
import requests

class KayakoMCPClient:
    def __init__(self, mcp_bridge_url="http://localhost:3000/mcp"):
        self.bridge_url = mcp_bridge_url
    
    def fetch_ticket_details(self, ticket_id: int):
        """Fetch ticket via MCP API bridge."""
        response = requests.post(
            f"{self.bridge_url}/kayako-oauth/fetch_ticket_details",
            json={"ticket_id": str(ticket_id)}
        )
        response.raise_for_status()
        return response.json()
```

### Option 3: Hybrid (Current + Fallback)

Keep current direct API calls, add MCP as enhancement:

```python
class KayakoMonitorService:
    def __init__(self, kayako_user, kayako_password, use_mcp=False):
        self.kayako_user = kayako_user
        self.kayako_password = kayako_password
        self.use_mcp = use_mcp
        
        if use_mcp:
            self.mcp_client = KayakoMCPClient()
        else:
            self.session = requests.Session()
    
    def fetch_ticket_data(self, ticket_id):
        """Fetch ticket - MCP or direct API."""
        if self.use_mcp:
            return self.mcp_client.fetch_ticket_details(ticket_id)
        else:
            return self._fetch_via_api(ticket_id)
```

## 🎁 Benefits of MCP Integration

### 1. Richer Data

**Before (Direct API):**
```json
{
  "id": 60144273,
  "subject": "Spanish login issue",
  "status": {"type": "hold", "label": "Hold"}
}
```

**After (MCP):**
```json
{
  "id": 60144273,
  "subject": "[00443499] Spanish version of site login loop",
  "status": "Hold",
  "priority": "High",
  "requester": {
    "name": "Heaven McCullough",
    "email": "heaven.stephenson6@t-mobile.com",
    "organization": "T-Mobile USA, Inc."
  },
  "product": {
    "product_name": "Khoros Community Aurora",
    "business_unit": "Khoros"
  },
  "jira_link": "KPSSUPPORT-55",
  "has_attachments": true,
  "post_count": 44,
  "translog": {
    "2025-12-25": "PS team still investigating...",
    // Complete history
  }
}
```

### 2. No Session Management

```python
# Before: Manual session handling
session = requests.Session()
auth_response = session.post(auth_url, data=creds)
session_id = auth_response.json()['session_id']
session.headers['X-Session-ID'] = session_id

# After: MCP handles it
result = mcp_client.fetch_ticket_details(ticket_id)
```

### 3. Advanced Features

```python
# Find similar tickets (semantic search)
similar = mcp_client.get_similar_tickets(ticket_id)

# Get organization from NetSuite AND Salesforce
org_data = mcp_client.search_organization_both("T-Mobile")

# Add internal note
mcp_client.add_internal_note(ticket_id, "Investigating issue...")

# Apply macro
mcp_client.send_to_external_team_macro(
    ticket_id=ticket_id,
    external_team="Engineering",
    key="JIRA-123",
    offset=24
)
```

## 📝 Example: Enhanced Monitoring

```python
class EnhancedKayakoMonitor:
    def __init__(self, kayako_user, kayako_password):
        self.kayako_user = kayako_user
        self.kayako_password = kayako_password
        self.mcp = KayakoMCPClient()
        self.tracker = CaseTracker()
    
    def check_dashboard(self, dashboard_id):
        """Check dashboard with MCP enrichment."""
        
        # Step 1: Scrape dashboard for case IDs
        case_ids = self._scrape_dashboard(dashboard_id)
        logger.info(f"Found {len(case_ids)} cases in dashboard")
        
        # Step 2: Enrich each case via MCP
        enriched_cases = []
        for case_id in case_ids:
            try:
                # Get rich details from MCP
                case_data = self.mcp.fetch_ticket_details(case_id)
                
                # Parse into our case object
                case = EnhancedCase(
                    id=case_data['id'],
                    subject=case_data['subject'],
                    status=case_data['status'],
                    priority=case_data['priority'],
                    requester=case_data['requester']['name'],
                    requester_email=case_data['requester']['email'],
                    organization=case_data['organization'],
                    product=case_data['product']['product_name'],
                    jira_link=case_data.get('jira_link'),
                    post_count=case_data['post_count'],
                    has_attachments=case_data['has_attachments']
                )
                
                enriched_cases.append(case)
                
                # Step 3: Check if new and notify
                if self.tracker.is_new_case(case):
                    self.notify_new_case(case)
                    
                    # Optional: Find similar past tickets
                    similar = self.mcp.get_similar_tickets(case_id)
                    if similar:
                        logger.info(f"Found {len(similar)} similar tickets")
                
            except Exception as e:
                logger.error(f"Error enriching case {case_id}: {e}")
        
        return enriched_cases
    
    def notify_new_case(self, case):
        """Send rich notification with MCP data."""
        notification = {
            'title': f'New Case: {case.subject}',
            'body': f"""
                Customer: {case.requester} ({case.organization})
                Product: {case.product}
                Priority: {case.priority}
                Status: {case.status}
                Jira: {case.jira_link or 'None'}
                Messages: {case.post_count}
            """,
            'url': f'https://central-supportdesk.kayako.com/agent/conversations/view/{case.id}'
        }
        
        self.send_notification(notification)
```

## 🚀 Next Steps

### Quick Win: Add MCP for Existing Cases

Enhance your current tool without changing the core logic:

1. Keep Selenium scraping as-is
2. Add MCP client for ticket enrichment
3. Use MCP data for richer notifications
4. Gradually add advanced features (similar tickets, CRM lookup)

### Files to Modify

- `app.py` → Add `KayakoMCPClient` class
- `fetch_dashboard_cases()` → Call MCP after getting case IDs
- `_parse_case()` → Use MCP response structure
- `notify_new_case()` → Include rich MCP data

### Testing

```bash
# Run the test script to see MCP capabilities
python3 test_mcp_fetch.py

# Try the MCP-enhanced version
python3 app_mcp.py
```

## 📚 References

- **MCP Tools Available**: See the function list at the top of this document
- **Example Ticket Data**: Run `test_mcp_fetch.py` to see structure
- **Current Implementation**: `app.py` (Selenium-based)
- **MCP Enhanced**: `app_mcp.py` (Hybrid approach)

## 🤔 FAQ

**Q: Can I use MCP without Selenium?**
A: Not for dashboard monitoring. MCP can't query by dashboard, so you still need Selenium to discover case IDs.

**Q: Does MCP replace my current API calls?**
A: It can, but hybrid is recommended. Keep Selenium for discovery, use MCP for enrichment.

**Q: Do I need Cursor to use MCP?**
A: For direct MCP access, yes. Alternatively, create an API bridge to use MCP from standalone scripts.

**Q: What about rate limits?**
A: MCP handles rate limiting automatically with retries.

**Q: Can I create tickets via MCP?**
A: Yes! `create_ticket` with auto-resolution of brands, teams, products.

---

**Ready to integrate? Start with `app_mcp.py` and `test_mcp_fetch.py`!** 🚀



