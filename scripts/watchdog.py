#!/usr/bin/env python3
"""
Watchdog script for gh-search team
Sends hourly reminders to PO to check team progress
"""

import subprocess
import time
from datetime import datetime

def send_to_po(message: str):
    """Send message to PO via tmux send-keys"""
    # Get PO pane ID from gh-search-team session
    try:
        # Find PO pane in gh-search-team session
        result = subprocess.run(
            ["tmux", "list-panes", "-a", "-F", "#{pane_id} #{@role_name} #{session_name}"],
            capture_output=True,
            text=True,
            check=True
        )

        po_pane = None
        for line in result.stdout.splitlines():
            parts = line.split()
            if len(parts) >= 3 and parts[1] == "PO" and parts[2] == "gh-search-team":
                po_pane = parts[0]
                break

        if not po_pane:
            print("✗ PO pane not found in gh-search-team session")
            return False

        # Send message using tmux send-keys (two-enter rule)
        subprocess.run(["tmux", "send-keys", "-t", po_pane, message, "C-m"], check=True)
        subprocess.run(["tmux", "send-keys", "-t", po_pane, "C-m"], check=True)

        print(f"✓ Message sent to PO at {datetime.now().strftime('%H:%M:%S')}")
        return True

    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to send message: {e}")
        return False

def get_watchdog_message() -> str:
    """Generate watchdog message"""
    now = datetime.now().strftime("%H:%M")

    message = f"""WATCHDOG [{now}]: Hourly Team Check

📋 Action Items for PO:
1. Check if team is sleeping or stuck
2. Check README fetch progress (target: 55,000 repos)
3. Take action if needed:
   - Technical issues → Ask Tech Lead
   - Decision needed → PO decides
   - Continue work if all OK

📚 Reminder for ALL roles:
- PO: Re-read WORKFLOW.md + prompts/PO_PROMPT.md
- TL: Re-read WORKFLOW.md + prompts/TL_PROMPT.md
- DEV: Re-read WORKFLOW.md + prompts/DEV_PROMPT.md

🎯 Goal: Complete all 55,000 GitHub repos

Please check status and continue work."""

    return message

def main():
    """Main watchdog loop - runs every hour"""
    print("🐕 Watchdog started - monitoring gh-search team")
    print("⏰ Sending reminders every 1 hour")
    print("Press Ctrl+C to stop\n")

    while True:
        message = get_watchdog_message()
        send_to_po(message)

        # Sleep for 1 hour (3600 seconds)
        print(f"💤 Sleeping for 1 hour... (next check at {datetime.now().strftime('%H:%M')})")
        time.sleep(3600)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Watchdog stopped by user")
    except Exception as e:
        print(f"❌ Watchdog error: {e}")
