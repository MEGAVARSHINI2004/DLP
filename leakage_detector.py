from detection.regex_detector import scan_text_for_sensitive_data
from detection.policy_engine import apply_policy
from modules.leak_reporter import save_leak
from detection.behavioral_analysis import BehaviorTracker

def detect_sensitive_data(text, source="ManualTest"):
    tracker = BehaviorTracker()
    findings = scan_text_for_sensitive_data(text)
    for label, matches in findings:
        action = apply_policy(source.lower(), label)
        save_leak(source, label, action, matches)
        tracker.record_access()
    if tracker.is_abnormal():
        save_leak("Behavior", "Abnormal Activity", "ALERT", ["Excessive activity detected"])

# Example usage
if __name__ == "__main__":
    test_data = """
    My email is test@example.com
    PAN: ABCDE1234F
    Aadhaar: 1234 5678 9012
    password: MySuperSecret123
    api_key: 123456abcdef
    """
    detect_sensitive_data(test_data, source="ManualTest")
