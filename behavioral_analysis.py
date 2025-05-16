import time
from collections import deque

class BehaviorTracker:
    def __init__(self, time_window=300, threshold=10):
        self.time_window = time_window  # in seconds
        self.threshold = threshold
        self.access_log = deque()

    def record_access(self):
        now = time.time()
        self.access_log.append(now)
        self.cleanup(now)

    def cleanup(self, now):
        while self.access_log and (now - self.access_log[0]) > self.time_window:
            self.access_log.popleft()

    def is_abnormal(self):
        return len(self.access_log) >= self.threshold
