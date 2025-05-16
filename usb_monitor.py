import psutil
import time

from detection.policy_engine import apply_policy
from detection.behavioral_analysis import BehaviorTracker
from modules.leak_reporter import save_leak

def get_usb_drives():
    drives = []
    for part in psutil.disk_partitions(all=False):
        if 'removable' in part.opts or 'cdrom' in part.opts:
            drives.append(part.device)
    return drives

def start_usb_monitor(tracker=None):
    tracker = tracker or BehaviorTracker()
    print("🔌 USB monitoring started...")
    known = set(get_usb_drives())

    try:
        while True:
            current = set(get_usb_drives())
            new_drives = current - known
            if new_drives:
                for drive in new_drives:
                    print(f"🚨 [ALERT] USB Drive Connected: {drive}")
                    save_leak("USB", "Device Plugged", "ALERT", [drive])
                    tracker.record_access()
                    if tracker.is_abnormal():
                        print("⚠️ Abnormal USB behavior detected!")
            known = current
            time.sleep(5)
    except KeyboardInterrupt:
        print("🛑 USB monitoring stopped.")
