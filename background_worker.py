import threading
import time

def run_background(job_fn, interval=300):
    def loop():
        while True:
            job_fn()
            time.sleep(interval)

    t = threading.Thread(target=loop, daemon=True)
    t.start()