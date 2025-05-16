import re

SENSITIVE_PATTERNS = {
    "email": r"[a-zA-Z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}",
    "password": r"\b(password|pwd|passcode|credentials)\b.*",
    "credit_card": r"\b(?:\d[ -]*?){13,16}\b",
    "api_key": r"(?i)(apikey|token|key)\s*[:=]?\s*\S+",
    "aadhar": r"\b\d{4}\s\d{4}\s\d{4}\b"
}

def scan_text_for_sensitive_data(text):
    findings = []
    for label, pattern in SENSITIVE_PATTERNS.items():
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            findings.append((label, matches))
    return findings
