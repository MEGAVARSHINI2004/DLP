import json
import os

POLICY_FILE = "policy_config.json"

DEFAULT_POLICY = {
    "email": {"block_on": ["password", "api_key"], "log_only": ["email"]},
    "clipboard": {"block_on": ["credit_card", "aadhar", "password"], "log_only": ["email"]},
    "file": {"block_on": ["password", "api_key", "credit_card", "aadhar"], "log_only": ["email"]},
    "usb": {"read_only_on_detection": True}
}

def load_policy():
    if os.path.exists(POLICY_FILE):
        with open(POLICY_FILE, 'r') as f:
            return json.load(f)
    return DEFAULT_POLICY

policy = load_policy()

def apply_policy(source, data_type):
    source_policy = policy.get(source.lower(), {})
    if data_type.lower() in map(str.lower, source_policy.get("block_on", [])):
        return "ALERT"
    elif data_type.lower() in map(str.lower, source_policy.get("log_only", [])):
        return "LOG"
    else:
        return "IGNORE"
