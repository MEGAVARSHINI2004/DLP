import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from detection.regex_detector import scan_text_for_sensitive_data
from detection.policy_engine import apply_policy
from detection.behavioral_analysis import BehaviorTracker
from modules.leak_reporter import save_leak

class FileEventHandler(FileSystemEventHandler):
    def __init__(self, tracker):
        self.tracker = tracker

    def process_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                findings = scan_text_for_sensitive_data(content)
                for label, matches in findings:
                    action = apply_policy("file", label)
                    save_leak("File", label, action, matches)
                    if action == "ALERT":
                        print(f"🚨 [ALERT] File Leak - {label}: {matches}")
                    self.tracker.record_access()
                if self.tracker.is_abnormal():
                    print("⚠️ Abnormal file access behavior detected!")
        except Exception as e:
            print(f"❌ Error reading file: {file_path} - {e}")

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(".txt"):
            print(f"[FileMonitor] Modified: {event.src_path}")
            self.process_file(event.src_path)

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".txt"):
            print(f"[FileMonitor] Created: {event.src_path}")
            self.process_file(event.src_path)

def start_file_monitor(path_to_watch="C:/SecureVaultWatch", tracker=None):
    print("📁 File monitoring started...")
    tracker = tracker or BehaviorTracker()
    event_handler = FileEventHandler(tracker)
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
