import subprocess
import requests
import time
import os
import threading

# ===== CONFIG =====
WEBHOOK_URL = "Put your Webhook APP LINK HERE"
SERVER_PORT = 19132
SERVER_PATH = r"Put your FILE Directory HERE"

# ===== PLAYER COUNT CONFIG =====
MAX_PLAYERS  = 10   # Match this to max-players in server.properties

# ===== PING CONFIG =====
PING_ON_ONLINE  = "<@&YOUR_ROLE"   # Who to ping when server is ONLINE
PING_ON_OFFLINE = "<@&YOUR_ROLE>"   # Who to ping when server is OFFLINE
PING_ON_CRASH   = "<@&YOUR_ROLE>"   # Who to ping when server CRASHES

server_started = False
player_count   = 0
players_online = []

def get_tailscale_ip():
    try:
        result = subprocess.run(
            ["tailscale", "ip", "-4"],
            capture_output=True, text=True
        )
        return result.stdout.strip()
    except:
        return "Unable to get Tailscale IP"

def send_discord(title, description, color, ping=""):
    """Send a Discord webhook message with optional ping."""
    payload = {
        # Ping is sent as plain content so Discord actually notifies the user
        "content": ping if ping else "",
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
    global server_started, player_count, players_online

    tailscale_ip = get_tailscale_ip()

    # Send Starting notification (no ping)
    send_discord(
        title="🟡 Server is Starting...",
        description=(
            f"**Tailscale IP:** `{tailscale_ip}`\n"
            f"**Port:** `{SERVER_PORT}`\n"
            f"**Status:** Starting up, please wait..."
        ),
        color=0xFFA500
    )

    # Start Minecraft Server
    print("Starting Minecraft Bedrock Server...")
    process = subprocess.Popen(
        SERVER_PATH,
        cwd=os.path.dirname(SERVER_PATH),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    for line in process.stdout:
        print(line, end="")

        # Server fully started
        if "Server started." in line and not server_started:
            server_started = True

            send_discord(
                title="🟢 Server is Online!",
                description=(
                    f"**Tailscale IP:** `{tailscale_ip}`\n"
                    f"**Port:** `{SERVER_PORT}`\n"
                    f"**Players:** `{player_count}/{MAX_PLAYERS}`\n\n"
                    f"**How to join:**\n"
                    f"```\nIP: {tailscale_ip}\nPort: {SERVER_PORT}\n```"
                ),
                color=0x00FF00,
                ping=PING_ON_ONLINE
            )

        # Player joined
        if "Player connected:" in line:
            player = line.split("Player connected:")[-1].strip().split(",")[0]
            player_count += 1
            players_online.append(player)

            send_discord(
                title="✅ Player Joined",
                description=(
                    f"**{player}** joined the server!\n"
                    f"**Players Online:** `{player_count}/{MAX_PLAYERS}`\n"
                    f"**Online Now:** "
                    f"{', '.join(players_online) if players_online else 'None'}"
                ),
                color=0x00BFFF
            )

        # Player left
        if "Player disconnected:" in line:
            player = line.split("Player disconnected:")[-1].strip().split(",")[0]
            player_count = max(0, player_count - 1)
            if player in players_online:
                players_online.remove(player)

            send_discord(
                title="👋 Player Left",
                description=(
                    f"**{player}** left the server.\n"
                    f"**Players Online:** `{player_count}/{MAX_PLAYERS}`\n"
                    f"**Still Online:** "
                    f"{', '.join(players_online) if players_online else 'None'}"
                ),
                color=0xFF6347
            )

    process.wait()
    # For debugging purposes
    print(f"[DEBUG] Server exited with code: {process.returncode}")

# Server stopped
    server_started = False
    player_count   = 0
    players_online = []
    # Fix unwanted crashes
    clean_exit_codes = [0, 1]

    if process.returncode in clean_exit_codes:
        send_discord(
            title="🔴 Server Stopped",
            description="The Minecraft server has been shut down normally.",
            color=0xFF0000,
            ping=PING_ON_OFFLINE
        )
    else:
        send_discord(
            title="💥 Server Crashed!",
            description=(
                f"The server stopped unexpectedly!\n"
                f"**Exit code:** `{process.returncode}`\n"
                f"Please check your server for errors."
            ),
            color=0x8B0000,
            ping=PING_ON_CRASH
        )
if __name__ == "__main__":
    main()


# Basic Executable on cmd
# cd D:\mc(1.26.14.1)(RL-Server)
# python start_server.py 
# or
# run it As it is
# Have fun using this simple Utility
# Version 2.0
# with player count! 