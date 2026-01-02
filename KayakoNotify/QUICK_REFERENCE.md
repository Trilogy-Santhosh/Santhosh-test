# 🚀 QUICK REFERENCE - Kayako Automated Monitor

## ✅ Is It Working?

**Check these 3 things:**

1. **Flask running?**
   ```bash
   curl http://localhost:8080/api/status
   # Should return: {"status": "running", ...}
   ```

2. **Case is Open?**
   - Go to Kayako dashboard
   - Check Status = "Open" (NOT Pending, Completed, etc.)

3. **Browser refreshed?**
   - Hard refresh: **Cmd + Shift + R** (Mac) or **Ctrl + Shift + R** (Windows)

---

## 📋 Your Filter Criteria

| Dashboard | Product | Form ID | Status |
|-----------|---------|---------|--------|
| **139** (Classic) | `khoros_classic` | 257 | Open |
| **143** (Aurora) | `khoros_aurora` | 258 | Open |

**Logic:** `(Form = X OR Product = Y) AND Status = Open`

---

## 🎯 Common Commands

### Start Flask App
```bash
cd /Users/santhosh.m/Documents/GitHub/Santhosh-test/KayakoNotify
python3 app_mcp.py
```

### Manually Push a Case
```bash
# For Classic (dashboard 139):
python3 push_real_case.py <CASE_ID> 139

# For Aurora (dashboard 143):
python3 push_aurora_case.py <CASE_ID> 143
```

### Check Logs
```bash
tail -f /Users/santhosh.m/Documents/GitHub/Santhosh-test/KayakoNotify/auto_monitor.log
```

### Stop All
```bash
pkill -f app_mcp
pkill -f auto_monitor
```

---

## 🐛 Troubleshooting

### Case not appearing?

1. ✅ Is case Status = "Open"? (Check Kayako)
2. ✅ Is Flask running? (`curl http://localhost:8080/api/status`)
3. ✅ Did you hard refresh browser? (Cmd+Shift+R)
4. ✅ Check product matches: Classic or Aurora?
5. ✅ Check logs: `tail -f auto_monitor.log`

### Port 8080 already in use?

```bash
# Find process using port 8080
lsof -i :8080

# Kill it
kill -9 <PID>

# Restart Flask
python3 app_mcp.py
```

### Flask crashes?

```bash
# Restart service
cd /Users/santhosh.m/Documents/GitHub/Santhosh-test/KayakoNotify
bash restart_service.sh
```

---

## 📖 Documentation Files

| File | What It Is |
|------|------------|
| `AUTOMATION_COMPLETE.md` | ⭐ Main summary - start here |
| `AUTO_MONITOR_GUIDE.md` | 📚 Detailed setup guide |
| `VISUAL_AUTOMATION_GUIDE.md` | 🎨 Diagrams and flow charts |
| `QUICK_REFERENCE.md` | 🚀 This file - quick commands |

---

## 🎊 Success Indicators

You'll know it's working when:
- ✅ New Open case in Kayako
- ✅ Within 90 seconds, appears in browser
- ✅ Desktop notification pops up
- ✅ Sound plays
- ✅ Case details show correctly

---

## 📞 Need Help?

1. Check logs: `tail -f auto_monitor.log`
2. Check Flask status: `curl http://localhost:8080/api/status`
3. Read full guide: `AUTO_MONITOR_GUIDE.md`
4. Test manually: `python3 push_real_case.py <CASE_ID> <DASHBOARD_ID>`

---

**Remember:** Cases must be **Open** status to appear! Pending/Completed won't match the filter.

