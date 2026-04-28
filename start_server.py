import subprocess
import requests
import socket
import time
import os

# ===== CONFIG =====
WEBHOOK_URL = "Put your Webhook APP LINK HERE"
SERVER_PORT = 19132
SERVER_PATH = r"Put your FILE Directory HERE"
# ==================

def get_tailscale_ip():
    try:
        result = subprocess.run(
            ["tailscale", "ip", "-4"],
            capture_output=True, text=True
        )
        return result.stdout.strip()
    except:
        return "Unable to get Tailscale IP"

def send_discord(title, description, color):
    payload = {
        "embeds": [{
            "title": title,
            "description": description,
            "color": color,
            "footer": {"text": "Minecraft Bedrock Server"},
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }]
    }
    requests.post(WEBHOOK_URL, json=payload)

def main():
    tailscale_ip = get_tailscale_ip()

    # Send Server Starting notification
    send_discord(
        title="🟡 Server is Starting...",
        description=(
            f"**Tailscale IP:** `{tailscale_ip}`\n"
            f"**Port:** `{SERVER_PORT}`\n"
            f"**Status:** Starting up, please wait..."
        ),
        color=0xFFA500  # Orange
    )

    # Start the Minecraft server
    print("Starting Minecraft Bedrock Server...")
    process = subprocess.Popen(
        SERVER_PATH,
        cwd=os.path.dirname(SERVER_PATH),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    server_started = False

    # Monitor the server output
    for line in process.stdout:
        print(line, end="")

        # Detect server fully started
        if "Server started." in line and not server_started:
            server_started = True
            send_discord(
                title="🟢 Server is Online!",
                description=(
                    f"**Tailscale IP:** `{tailscale_ip}`\n"
                    f"**Port:** `{SERVER_PORT}`\n\n"
                    f"**How to join:**\n"
                    f"Add server in Minecraft with:\n"
                    f"```\nIP: {tailscale_ip}\nPort: {SERVER_PORT}\n```"
                ),
                color=0x00FF00  # Green
            )

        # Detect player joined
        if "Player connected:" in line:
            player = line.split("Player connected:")[-1].strip().split(",")[0]
            send_discord(
                title="✅ Player Joined",
                description=f"**{player}** joined the server!",
                color=0x00BFFF  # Blue
            )

        # Detect player left
        if "Player disconnected:" in line:
            player = line.split("Player disconnected:")[-1].strip().split(",")[0]
            send_discord(
                title="👋 Player Left",
                description=f"**{player}** left the server.",
                color=0xFF6347  # Red-orange
            )

    # Server stopped/crashed
    process.wait()
    if process.returncode == 0:
        send_discord(
            title="🔴 Server Stopped",
            description="The Minecraft server has been shut down normally.",
            color=0xFF0000  # Red
        )
    else:
        send_discord(
            title="💥 Server Crashed!",
            description=(
                f"The server stopped unexpectedly!\n"
                f"**Exit code:** `{process.returncode}`\n"
                f"Please check your server for errors."
            ),
            color=0x8B0000  # Dark red
        )

if __name__ == "__main__":
    main()


# Basic Executable on cmd
# cd D:\mc(1.26.14.1)(RL-Server)
# python start_server.py 
# or
# run it As it is
# Have using this simple Utility 