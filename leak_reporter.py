import csv
import os
from datetime import datetime

REPORT_FILE = "leak_report.csv"

if not os.path.exists(REPORT_FILE):
    with open(REPORT_FILE, 'w', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        writer.writerow(["Timestamp", "Source", "Type", "Action", "Detected Data"])

def save_leak(source, data_type, action, data):
    if data:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(REPORT_FILE, 'a', newline='') as file:
            writer = csv.writer(file, quoting=csv.QUOTE_ALL)
            for item in data:
                writer.writerow([timestamp, source, data_type, action, item])
        print(f"[Leak Reporter] Leak saved: {source} - {data_type} - {action} - {data}")
    else:
        print(f"[Leak Reporter] No data detected for {data_type}.")
