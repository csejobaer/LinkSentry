import time

class SpeedMeter:
    def __init__(self):
        self.start = time.time()
        self.count = 0

    def tick(self):
        self.count += 1
        elapsed = time.time() - self.start + 0.001
        return round(self.count / elapsed, 2)
