# 🔔 Kayako Dashboard Notification Service

A **complete browser-based notification system** for monitoring Kayako support dashboards.

## 🎯 What It Does

Monitors these Kayako dashboards for new cases:
- **Dashboard 139** - Priority Support Cases
- **Dashboard 143** - Escalated Issues

When new cases arrive, you get:
- 🖥️ Desktop notifications
- 🔔 Browser notifications
- 📊 Real-time dashboard updates
- 🔊 Sound alerts (optional)

## ⚡ Quick Start

### 1. Install Dependencies

```bash
pip install flask requests
```

### 2. Start the Application

```bash
python3 app.py
```

### 3. Open in Browser

```
http://localhost:8080
```

### 4. Configure & Start

1. Enter your Kayako credentials in the web interface
2. Click "Save & Start Monitoring"
3. Watch for new cases in real-time!

## 🌐 Browser-Based Setup

Everything runs locally in your browser - no command line needed!

1. **Configuration** - Enter credentials via web form
2. **Monitoring** - Start/stop with buttons
3. **Real-time Updates** - See new cases as they arrive
4. **Notifications** - Get desktop and browser alerts

## 📊 Features

✅ **100% Browser-Based** - No terminal commands  
✅ **Real-time Dashboard** - Live case updates  
✅ **Multi-channel Notifications** - Desktop + Browser alerts  
✅ **Smart Tracking** - No duplicate notifications  
✅ **Beautiful UI** - Modern, responsive design  
✅ **Easy Configuration** - Web-based setup  

## 🎨 Screenshots

The dashboard shows:
- Service status (running/stopped)
- Total cases tracked
- New cases today
- Live case list with details
- Control buttons (start/stop/refresh)

## 🔧 How It Works

```
1. Start the Flask app (python3 app.py)
2. Open http://localhost:8080 in your browser
3. Enter Kayako credentials
4. Click "Start Monitoring"
5. App checks dashboards every 60 seconds
6. New cases trigger notifications
```

## 📱 Access from Any Device

The web interface is accessible from:
- Your computer browser
- Other computers on your network (http://YOUR_IP:8080)
- Mobile devices
- Tablets

## 🔐 Security

- Credentials stored in memory only (not saved to disk)
- All API calls use HTTPS
- Runs locally on your machine
- No external data transmission

## 📦 Files

```
KayakoNotify/
├── app.py                    # Main Flask application
├── templates/
│   └── index.html           # Web dashboard UI
├── static/                  # Static files (optional)
└── README.md               # This file
```

## 🎯 Usage Tips

### Keep it Running in Background

```bash
# Using screen
screen -S kayako
python3 app.py
# Press Ctrl+A then D to detach

# Reattach later
screen -r kayako
```

### Change Check Interval

Edit `app.py`, find this line:
```python
self.check_interval = 60  # seconds
```

Change to 30 for faster checks:
```python
self.check_interval = 30  # seconds
```

### Add More Dashboards

Edit `app.py`, find the `api_start` function and add:
```python
notification_service.add_dashboard(150, "VIP Customers")
```

## 🐛 Troubleshooting

### Can't access from other devices?

Make sure your firewall allows port 8080.

### Notifications not showing?

Click "Allow" when browser asks for notification permission.

### Service not starting?

Check your Kayako credentials are correct.

## 📞 Support

If something doesn't work:
1. Check the browser console (F12) for errors
2. Check the terminal where `app.py` is running
3. Verify your Kayako credentials are correct

## 🎉 You're All Set!

Just run `python3 app.py` and open http://localhost:8080 in your browser!

**Enjoy your automatic Kayako notifications!** 🔔

