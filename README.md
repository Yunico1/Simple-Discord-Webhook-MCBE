# 🎮 Minecraft Bedrock Dedicated Server + Tailscale + Discord Notifications

A simple Python script that starts your Minecraft Bedrock Dedicated Server and sends real-time notifications to Discord via webhook — including your Tailscale IP so your friends always know how to connect.

---

## ✨ Features

- 🟡 Notifies Discord when server is **starting**
- 🟢 Notifies Discord when server is **online** with your Tailscale IP and port
- ✅ Notifies Discord when a **player joins**
- 👋 Notifies Discord when a **player leaves**
- 🔴 Notifies Discord when server **stops normally**
- 💥 Notifies Discord when server **crashes** with exit code

---

## ✨ Features V2.0
- 👥 Notifies Discord how many players are currently playing
- ❗ Notifies Discord roles assigned

---

## 📋 Requirements

- Windows PC
- [Minecraft Bedrock Dedicated Server](https://www.minecraft.net/en-us/download/server/bedrock)
- [Tailscale](https://tailscale.com/download) installed and running
- [Python 3.x](https://python.org/downloads) (make sure to check **Add Python to PATH** during install)
- A Discord server with a Webhook URL

---

## 📦 Installation

### 1. Clone or Download this Repository
Place `start_server.py` inside your Minecraft Bedrock server folder:
```
D:\YourServerFolder\
    bedrock_server.exe
    server.properties
    start_server.py     ← place it here
    worlds\
    ...
```

### 2. Install Required Libraries
Open **Command Prompt** and run:
```bash
pip install requests psutil
```

### 3. Create a Discord Webhook
1. Open your Discord server
2. Go to the channel you want notifications in
3. Click the ⚙️ gear icon next to the channel → **Integrations** → **Webhooks**
4. Click **New Webhook** → name it → click **Copy Webhook URL**

### 4. Configure the Script
Open `start_server.py` with Notepad and update these two lines:

```python
WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL_HERE"  # Paste your webhook URL here
SERVER_PATH = r"D:\YourServerFolder\bedrock_server.exe"  # Path to your server
```

---

## 🚀 Usage

> ⚠️ **Always run Command Prompt as Administrator**

1. Make sure **Tailscale is running** in your system tray
2. Open **Command Prompt as Administrator**
3. Navigate to your server folder:
```bash
cd D:\YourServerFolder
```
4. Start the server:
```bash
python start_server.py
```
5. Wait for the 🟢 **green Discord notification** before telling friends to join!

---

## 👥 For Your Friends

All friends must have **Tailscale installed and connected** before joining.

| Platform | Download |
|----------|----------|
| Windows | [tailscale.com/download](https://tailscale.com/download) |
| Android | Google Play Store → search **Tailscale** |
| iOS | App Store → search **Tailscale** |

Once connected to Tailscale, add the server in Minecraft:
- **IP:** Your Tailscale IP (shown in the Discord notification, starts with `100.x.x.x`)
- **Port:** `19132`

---

## 📡 Discord Notification Preview

| Event | Color | Message |
|-------|-------|---------|
| Server Starting | 🟡 Orange | Tailscale IP + status |
| Server Online | 🟢 Green | Tailscale IP + how to join |
| Player Joined | 🔵 Blue | Player name |
| Player Left | 🟠 Red-Orange | Player name |
| Server Stopped | 🔴 Red | Shutdown message |
| Server Crashed | 💥 Dark Red | Exit code + error info |

## ✨ Features V2.0

When someone joins the server

| Players | 1/10 | Message |
| John Doe | ✅ | John Doe Join the server |

When someone leaves the server

| Players | 0/10 | Message |
| John Doe | 👋 | John Doe Left the server |

---

## ❓ Troubleshooting

**PermissionError: [WinError 5] Access is denied**
→ Run Command Prompt as **Administrator**

**Tailscale IP shows "Unable to get Tailscale IP"**
→ Make sure Tailscale is running in your system tray before starting the script

**Friends can't connect**
→ Make sure they have Tailscale **connected** on their device before joining
→ Double check they're using the correct `100.x.x.x` IP and port `19132`

**Port forwarding won't work**
→ Check if your ISP uses **CGNAT** — if so, Tailscale is the correct solution (no port forwarding needed)

---

## 📝 Notes

- You do **not** need to set up port forwarding on your router when using Tailscale
- Your Tailscale IP (`100.x.x.x`) is permanent and rarely changes
- Tailscale free plan supports up to **6 users** with unlimited bandwidth

---

## 📄 License

This project is free to use and modify for personal use.

---

> Made with ❤️ for Minecraft Bedrock players who just want to play with friends.
