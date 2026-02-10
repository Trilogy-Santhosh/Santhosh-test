# 🤖 AUTOMATED KAYAKO MONITOR - SETUP GUIDE

## 🎯 What This Does

**FULLY AUTOMATED** case monitoring that:
- ✅ Fetches cases from Kayako every 60 seconds
- ✅ Filters them by your criteria
- ✅ Pushes matching cases to your browser tool
- ✅ Notifies you when new cases appear
- ✅ NO MANUAL INTERVENTION NEEDED!

---

## 📋 Your Filtering Criteria

### Dashboard 139: Khoros Classic Community
```
(Form = "Khoros Classic Community Support" (ID: 257) OR Product = "khoros_classic")
AND Status = "Open"
```

### Dashboard 143: Khoros Aurora
```
(Form = "Khoros Aurora Community Support" (ID: 254) OR Product = "khoros_aurora")
AND Status = "Open"
```

---

## 🔧 How It Works

### Architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                    KAYAKO (Source)                          │
│  Dashboards 139 & 143 with Open cases                      │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          │ Every 60 seconds
                          ↓
┌─────────────────────────────────────────────────────────────┐
│            AUTO MONITOR (Python + MCP)                      │
│                                                             │
│  1. Fetch all open tickets via MCP                         │
│  2. Get full details for each                              │
│  3. Filter by:                                              │
│     - Dashboard 139: Form=257 OR Product=khoros_classic    │
│     - Dashboard 143: Form=254 OR Product=khoros_aurora     │
│  4. Must have Status = "Open"                              │
│                                                             │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          │ HTTP POST
                          ↓
┌─────────────────────────────────────────────────────────────┐
│            FLASK APP (app_mcp.py)                           │
│  Running at http://localhost:8080                          │
│                                                             │
│  - Receives cases via /api/mcp/fetch                       │
│  - Stores in case_cache                                    │
│  - Tracks new vs. updated                                  │
│                                                             │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          │ WebSocket / Polling
                          ↓
┌─────────────────────────────────────────────────────────────┐
│          BROWSER (Your Tool)                                │
│                                                             │
│  - Auto-refreshes every 30 seconds                         │
│  - Shows cases for each dashboard                          │
│  - Desktop notification for new cases                      │
│  - Sound alert                                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Option A: Manual Testing (Available NOW)

Since your cases are currently **Pending** (you moved them!), let's verify the logic:

1. **Fetch a historical case to verify structure:**
   ```python
   # In Cursor, run this in Python:
   # This fetches case #60269686 (the Classic case you mentioned)
   ```

2. **Wait for a NEW Open case to appear in dashboard 139 or 143**

3. **Manually push it to test:**
   ```bash
   cd /Users/santhosh.m/Documents/GitHub/Santhosh-test/KayakoNotify
   python3 push_real_case.py <CASE_ID> <DASHBOARD_ID>
   ```

### Option B: Full Automation (Requires Setup)

**Prerequisites:**
- ✅ Flask app running: `python3 app_mcp.py`
- ✅ MCP integration in Cursor AI
- ✅ Access to Kayako OAuth MCP tools

**Steps:**

1. **Create a wrapper script** that Cursor AI will use to invoke MCP:

   ```bash
   cd /Users/santhosh.m/Documents/GitHub/Santhosh-test/KayakoNotify
   python3 auto_monitor_live.py
   ```

2. **Set up automation** (choose one):

   **A) Cron job (runs every 60 seconds):**
   ```bash
   # Edit crontab
   crontab -e
   
   # Add this line:
   * * * * * cd /Users/santhosh.m/Documents/GitHub/Santhosh-test/KayakoNotify && /usr/bin/python3 auto_monitor_live.py >> auto_monitor.log 2>&1
   ```

   **B) Background process:**
   ```bash
   cd /Users/santhosh.m/Documents/GitHub/Santhosh-test/KayakoNotify
   nohup python3 auto_monitor_mcp.py &
   ```

   **C) macOS LaunchAgent (recommended):**
   Create: `~/Library/LaunchAgents/com.kayako.monitor.plist`
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
       <key>Label</key>
       <string>com.kayako.monitor</string>
       <key>ProgramArguments</key>
       <array>
           <string>/usr/bin/python3</string>
           <string>/Users/santhosh.m/Documents/GitHub/Santhosh-test/KayakoNotify/auto_monitor_mcp.py</string>
       </array>
       <key>StartInterval</key>
       <integer>60</integer>
       <key>StandardOutPath</key>
       <string>/Users/santhosh.m/Documents/GitHub/Santhosh-test/KayakoNotify/auto_monitor.log</string>
       <key>StandardErrorPath</key>
       <string>/Users/santhosh.m/Documents/GitHub/Santhosh-test/KayakoNotify/auto_monitor_error.log</string>
   </dict>
   </plist>
   ```
   
   Then:
   ```bash
   launchctl load ~/Library/LaunchAgents/com.kayako.monitor.plist
   launchctl start com.kayako.monitor
   ```

---

## 🧪 Testing Right Now

Since the cases in dashboard 139 are now **Pending**, let's verify with the Aurora case:

```bash
cd /Users/santhosh.m/Documents/GitHub/Santhosh-test/KayakoNotify
python3 push_aurora_case.py
```

Then **hard refresh your browser** (Cmd + Shift + R) and check dashboard 143!

---

## 📊 Monitoring & Logs

**Check if monitor is running:**
```bash
ps aux | grep auto_monitor
```

**View logs:**
```bash
tail -f /Users/santhosh.m/Documents/GitHub/Santhosh-test/KayakoNotify/auto_monitor.log
```

**Stop monitoring:**
```bash
# If using cron:
crontab -e  # Remove the line

# If using LaunchAgent:
launchctl stop com.kayako.monitor
launchctl unload ~/Library/LaunchAgents/com.kayako.monitor.plist

# If background process:
pkill -f auto_monitor
```

---

## 🎯 What Happens When a New Case Appears?

1. **Kayako**: New case created with Status = "Open"
2. **Monitor** (within 60 seconds):
   - Fetches all open tickets
   - Checks: Is Form=257/254 OR Product=khoros_classic/aurora?
   - Checks: Is Status="Open"?
   - If YES → Push to Flask
3. **Flask**: Receives case, stores in cache
4. **Browser** (within 30 seconds):
   - Polls Flask for updates
   - Detects new case
   - Shows notification 🔔
   - Plays sound 🔊
   - Displays case in UI

**Total delay: Up to 90 seconds** (60s monitor + 30s browser poll)

---

## ⚙️ Configuration

Edit the criteria in `auto_monitor_live.py`:

```python
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
        "form_ids": [254],  # Verify this!
        "status": "Open"
    }
}
```

**To change check interval:**
```python
CHECK_INTERVAL = 60  # Change to 30, 120, etc.
```

---

## 🔍 Troubleshooting

### No cases appearing?

1. **Check if Flask is running:**
   ```bash
   curl http://localhost:8080/api/status
   ```

2. **Check if monitor is running:**
   ```bash
   ps aux | grep auto_monitor
   ```

3. **Check logs:**
   ```bash
   tail -f auto_monitor.log
   ```

4. **Verify case is actually Open:**
   - Go to Kayako dashboard
   - Check if Status = "Open" (not Pending!)
   - Check if Product matches

5. **Manually test:**
   ```python
   # Fetch the case via MCP and inspect
   # Make sure Form ID and Product Tag match your criteria
   ```

### Form ID unknown?

If you're not sure about form ID 254 for Aurora, we can:
1. Fetch a known Aurora ticket
2. Check its `form.id` field
3. Update the config

---

## 📝 Next Steps

1. ✅ **Test current setup** - Hard refresh browser, check if Aurora case appears
2. ✅ **Verify form IDs** - Fetch a few tickets from each dashboard to confirm Form IDs
3. ✅ **Wait for new Open case** - Let a real case come in and watch it auto-appear!
4. ✅ **Set up automation** - Choose cron, LaunchAgent, or background process
5. ✅ **Enjoy notifications** - Sit back and get alerted automatically! 🎉

---

## 🎉 Success Criteria

You'll know it's working when:
- ✅ New Open case appears in Kayako dashboard 139 or 143
- ✅ Within 90 seconds, it appears in your browser tool
- ✅ You get a desktop notification
- ✅ You hear the alert sound
- ✅ Case shows correct details (subject, requester, priority, etc.)

**NO MANUAL PUSHING NEEDED!** 🚀



