
import time
import requests

class SimpleCircuitBreaker:
    def __init__(self, failure_threshold=3, reset_timeout=30):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.failures = 0
        self.state = "CLOSED"
        self.opened_at = None

    def call(self, func, *args, **kwargs):
        if self.state == "OPEN":
            if time.time() - self.opened_at < self.reset_timeout:
                raise RuntimeError("Circuit is OPEN, skipping call")
            else:
                self.state = "HALF_OPEN"

        try:
            result = func(*args, **kwargs)
        except Exception:
            self.failures += 1
            if self.failures >= self.failure_threshold:
                self.state = "OPEN"
                self.opened_at = time.time()
            raise
        else:
            self.failures = 0
            self.state = "CLOSED"
            return result


cb = SimpleCircuitBreaker()

def call_bank_api(amount):
    # Example call to an external bank API
    r = requests.post("https://bank.example.com/pay", json={"amount": amount}, timeout=2)
    r.raise_for_status()
    return r.json()

def safe_payment(amount):
    return cb.call(call_bank_api, amount)

