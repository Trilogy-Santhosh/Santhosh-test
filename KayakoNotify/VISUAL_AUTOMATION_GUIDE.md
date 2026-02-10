# 🎨 AUTOMATED KAYAKO MONITOR - VISUAL GUIDE

## 🏗️ System Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                        KAYAKO SYSTEM                               │
│                                                                    │
│  Dashboard 139: Khoros Classic Community                          │
│  └─ Filter: (Form=257 OR Product=khoros_classic) + Status=Open   │
│                                                                    │
│  Dashboard 143: Khoros Aurora                                     │
│  └─ Filter: (Form=258 OR Product=khoros_aurora) + Status=Open    │
│                                                                    │
└────────────────────────┬───────────────────────────────────────────┘
                         │
                         │ 📡 MCP OAuth Integration
                         │ (Kayako API calls)
                         ↓
┌────────────────────────────────────────────────────────────────────┐
│                    CURSOR AI + MCP TOOLS                           │
│                                                                    │
│  Available MCP Tools:                                             │
│  • fetch_ticket_details(ticket_id)                                │
│  • get_user_tickets(user_id)                                      │
│  • search via JQL                                                 │
│                                                                    │
└────────────────────────┬───────────────────────────────────────────┘
                         │
                         │ 🐍 Python Scripts
                         │
                         ↓
┌────────────────────────────────────────────────────────────────────┐
│              AUTO MONITOR (auto_monitor_live.py)                   │
│                                                                    │
│  Every 60 seconds:                                                │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │ 1. Fetch all Open tickets via MCP                        │    │
│  │ 2. Get full details for each                             │    │
│  │ 3. Apply filtering logic:                                │    │
│  │    Dashboard 139: Form=257 OR Product=khoros_classic     │    │
│  │    Dashboard 143: Form=258 OR Product=khoros_aurora      │    │
│  │    MUST have: Status = "Open"                            │    │
│  │ 4. Format cases for Flask                                │    │
│  │ 5. Push to Flask via HTTP POST                           │    │
│  └──────────────────────────────────────────────────────────┘    │
│                                                                    │
│  Tracks seen cases to detect NEW vs UPDATED                       │
│                                                                    │
└────────────────────────┬───────────────────────────────────────────┘
                         │
                         │ 📤 HTTP POST to /api/mcp/fetch
                         │ {dashboard_id: int, cases: [...]}
                         ↓
┌────────────────────────────────────────────────────────────────────┐
│                FLASK APP (app_mcp.py)                              │
│                Running on http://localhost:8080                    │
│                                                                    │
│  Endpoints:                                                       │
│  • POST /api/mcp/fetch        → Receive cases from monitor       │
│  • GET  /api/cases/<id>       → Browser fetches cases            │
│  • GET  /api/status           → Health check                     │
│                                                                    │
│  case_cache = {                                                   │
│    60273725: {                                                    │
│      case_id: 60273725,                                           │
│      dashboard_id: 143,                                           │
│      subject: "Error while migrating...",                         │
│      status: "Open",                                              │
│      product: "Khoros Community Aurora",                          │
│      ...                                                          │
│    }                                                              │
│  }                                                                │
│                                                                    │
└────────────────────────┬───────────────────────────────────────────┘
                         │
                         │ 📥 Browser polls every 30 seconds
                         │ GET /api/cases/139 and /api/cases/143
                         ↓
┌────────────────────────────────────────────────────────────────────┐
│                  BROWSER (Chrome/Safari/Firefox)                   │
│                  http://localhost:8080                             │
│                                                                    │
│  ┌──────────────────────────┬──────────────────────────┐         │
│  │   Dashboard 139          │   Dashboard 143          │         │
│  │   Khoros Classic         │   Khoros Aurora          │         │
│  │                          │                          │         │
│  │  [Case #60269686] ⏳     │  [Case #60273725] 🆕     │         │
│  │  Status: Pending         │  Status: Open            │         │
│  │  (Won't show - filtered) │  Subject: Error while... │         │
│  │                          │  Priority: High          │         │
│  │  Waiting for new Open... │  Requester: Anurag Das   │         │
│  └──────────────────────────┴──────────────────────────┘         │
│                                                                    │
│  🔔 Notification: "New case in Dashboard 143!"                    │
│  🔊 Sound: *ding*                                                 │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow Timeline

### Scenario: New Case Arrives

```
T+0s     │ Customer creates new case in Kayako
         │ • Subject: "Login not working"
         │ • Product: khoros_classic
         │ • Status: Open
         │ • Form: 257
         │
         ↓
T+0-60s  │ Auto Monitor: Next cycle runs
         │ • Fetches all open tickets
         │ • Gets full details for each
         │ • Applies filters
         │
         ↓
T+60s    │ Auto Monitor: Case matches Dashboard 139!
         │ • Form = 257 ✓
         │ • Product = khoros_classic ✓
         │ • Status = Open ✓
         │ • Formats case data
         │
         ↓
T+61s    │ Auto Monitor: POST to Flask
         │ POST /api/mcp/fetch
         │ {
         │   dashboard_id: 139,
         │   cases: [{case_id: 60275000, ...}]
         │ }
         │
         ↓
T+61s    │ Flask: Receives case
         │ • Checks case_cache
         │ • Case not seen before → marks as "new"
         │ • Stores in case_cache[60275000]
         │ • Returns: {new: 1, received: 1}
         │
         ↓
T+61-91s │ Browser: Next poll cycle
         │ • Fetches: GET /api/cases/139
         │ • Receives updated case list
         │ • Detects new case!
         │
         ↓
T+91s    │ Browser: Displays notification
         │ 🔔 Desktop notification appears
         │ 🔊 Sound plays
         │ 📝 Case appears in Dashboard 139
         │
         ↓
T+91s    │ YOU: See the case! 🎉
         │ • Click to open in Kayako
         │ • Start working on it
         │ • Mark as Pending when responded
```

**Total time: ≤ 90 seconds from case creation to notification!**

---

## 🎯 Filtering Logic Diagram

```
                    ┌─────────────────────┐
                    │  Kayako Ticket      │
                    │  (any status)       │
                    └──────────┬──────────┘
                               │
                               ↓
                    ┌─────────────────────┐
                    │  Status = "Open"?   │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
                   NO                    YES
                    │                     │
                    ↓                     ↓
            ❌ REJECT         ┌─────────────────────┐
                              │  Product Tag OR     │
                              │  Form ID match?     │
                              └──────────┬──────────┘
                                         │
                    ┌────────────────────┴────────────────────┐
                    │                                         │
                    ↓                                         ↓
          ┌─────────────────────┐                 ┌─────────────────────┐
          │  Dashboard 139?     │                 │  Dashboard 143?     │
          │                     │                 │                     │
          │  Form = 257?        │                 │  Form = 258?        │
          │  OR                 │                 │  OR                 │
          │  Product =          │                 │  Product =          │
          │  khoros_classic?    │                 │  khoros_aurora?     │
          └──────────┬──────────┘                 └──────────┬──────────┘
                     │                                       │
          ┌──────────┴──────────┐                 ┌──────────┴──────────┐
          │                     │                 │                     │
         YES                   NO                YES                   NO
          │                     │                 │                     │
          ↓                     ↓                 ↓                     ↓
    ✅ PUSH TO           ❌ REJECT         ✅ PUSH TO           ❌ REJECT
    DASHBOARD 139                         DASHBOARD 143
```

---

## 📊 Case Status Flow

```
┌─────────────┐
│   NEW       │  Customer creates case
│  (Status:   │
│   Open)     │
└──────┬──────┘
       │
       │ Within 90 seconds
       ↓
┌─────────────┐
│  APPEARS    │  Auto-detected and displayed
│  IN YOUR    │  🔔 Notification sent
│  BROWSER    │  🔊 Sound plays
└──────┬──────┘
       │
       │ You respond
       ↓
┌─────────────┐
│  PENDING    │  You mark as Pending
│  (Status:   │
│   Pending)  │
└──────┬──────┘
       │
       │ No longer matches filter!
       ↓
┌─────────────┐
│  REMOVED    │  Disappears from dashboard
│  FROM       │  (Status ≠ Open)
│  DASHBOARD  │
└─────────────┘
```

---

## 🔧 Configuration Map

```
auto_monitor_live.py
├── FLASK_URL = "http://localhost:8080"
├── CHECK_INTERVAL = 60  # seconds
└── DASHBOARDS = {
    139: {
        name: "Khoros Classic Community",
        product_tags: ["khoros_classic"],
        form_ids: [257],
        status: "Open"
    },
    143: {
        name: "Khoros Aurora",
        product_tags: ["khoros_aurora"],
        form_ids: [258],
        status: "Open"
    }
}

app_mcp.py
├── PORT = 8080
├── case_cache = {}  # {case_id: case_data}
└── Endpoints:
    ├── POST /api/mcp/fetch
    ├── GET  /api/cases/<dashboard_id>
    └── GET  /api/status

templates/index_mcp.html
├── Poll interval: 30 seconds
├── Notification: Web Notification API
└── Sound: /static/notification.mp3
```

---

## 🎉 End Result

```
┌────────────────────────────────────────────────────┐
│  YOU                                               │
│  ├── Open browser: http://localhost:8080          │
│  ├── See two dashboards (139 & 143)               │
│  ├── Cases auto-refresh every 30 seconds          │
│  ├── Get notifications for new cases              │
│  └── No manual work needed! 🚀                    │
└────────────────────────────────────────────────────┘
```

**Everything happens automatically!** 🎊



