import threading
import time
from modules.file_monitor import start_file_monitor
from modules.clipboard_monitor import monitor_clipboard
from modules.email_monitor import simulate_email_sending
from modules.usb_monitor import start_usb_monitor
from detection.behavioral_analysis import BehaviorTracker

def main():
    print("🔄 Initializing SecureVault Components...")
    tracker = BehaviorTracker(time_window=300, threshold=10)

    print("✅ SecureVault Monitoring Started...\n")

    watch_path = "C:/SecureVaultWatch"

    threading.Thread(target=start_file_monitor, args=(watch_path, tracker), daemon=True).start()
    print("📁 File monitoring started...")

    threading.Thread(target=monitor_clipboard, args=(tracker,), daemon=True).start()
    print("📋 Clipboard monitoring started...")

    threading.Thread(target=start_usb_monitor, args=(tracker,), daemon=True).start()
    print("🔌 USB monitoring started...")

    threading.Thread(target=simulate_email_sending, args=(tracker,), daemon=True).start()
    print("📧 Email monitoring started...\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("🔥 Stopping all monitoring services...")

if __name__ == "__main__":
    main()
