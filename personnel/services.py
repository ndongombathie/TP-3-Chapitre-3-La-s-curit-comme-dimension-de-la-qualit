from django.core.cache import cache

class LoginThrottle:
    
    def __init__(self, max_attempts: int = 5):
        self.max_attempts = max_attempts
        self.attempts = {}

    def enregistrer_tentative(self, username: str) -> None:
        self.attempts[username] = self.attempts.get(username, 0) + 1
        cache.set(f"login_throttle:{username}", self.attempts[username], timeout=60*15)  # expire après 15 minutes

    def est_bloque(self, username: str) -> bool:
        return cache.get(f"login_throttle:{username}", 0) >= self.max_attempts

    def reinitialiser_tentatives(self, username: str) -> None:
        cache.delete(f"login_throttle:{username}")