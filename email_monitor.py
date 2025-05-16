import time
from detection.regex_detector import scan_text_for_sensitive_data
from detection.policy_engine import apply_policy
from detection.behavioral_analysis import BehaviorTracker
from modules.leak_reporter import save_leak

def simulate_email_sending(tracker=None):
    tracker = tracker or BehaviorTracker()
    print("📧 Email monitoring started...")
    try:
        while True:
            content = input("📝 Type a fake email content (or type 'exit'):\n> ")
            if content.lower() == 'exit':
                break

            findings = scan_text_for_sensitive_data(content)
            if findings:
                for label, matches in findings:
                    action = apply_policy("email", label)
                    save_leak("Email", label, action, matches)
                    if action == "ALERT":
                        print(f"🚨 [ALERT] Email Leak - {label}: {matches}")
                    tracker.record_access()

                if tracker.is_abnormal():
                    print("⚠️ Abnormal email behavior detected!")
            else:
                print("✅ No sensitive keywords detected.")
            time.sleep(1)
    except KeyboardInterrupt:
        print("🛑 Email monitoring stopped.")
