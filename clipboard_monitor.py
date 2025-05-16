import pyperclip
import time

from detection.regex_detector import scan_text_for_sensitive_data
from detection.policy_engine import apply_policy
from detection.behavioral_analysis import BehaviorTracker
from modules.leak_reporter import save_leak

def monitor_clipboard(tracker=None):
    tracker = tracker or BehaviorTracker()
    print("📋 Clipboard monitoring started...")
    recent_value = ""

    try:
        while True:
            content = pyperclip.paste()
            if content != recent_value:
                recent_value = content
                print(f"[Clipboard Monitor] Detected new content:\n{content}")

                findings = scan_text_for_sensitive_data(content)
                for label, matches in findings:
                    action = apply_policy("clipboard", label)
                    save_leak("Clipboard", label, action, matches)
                    if action == "ALERT":
                        print(f"🚨 [ALERT] Clipboard Leak - {label}: {matches}")
                    tracker.record_access()

                if tracker.is_abnormal():
                    print("⚠️ Abnormal clipboard behavior detected!")
            time.sleep(2)
    except KeyboardInterrupt:
        print("🛑 Clipboard monitoring stopped.")
