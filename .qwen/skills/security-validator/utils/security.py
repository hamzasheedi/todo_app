from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Callable, Awaitable
import time
import hashlib
import asyncio
from collections import defaultdict, deque
from datetime import datetime, timedelta
import re

class SecurityMiddleware:
    """
    Comprehensive security middleware for the Todo application
    """

    def __init__(self):
        # Rate limiting storage: {ip: [(timestamp, count)]}
        self.rate_limit_storage = defaultdict(deque)
        self.rate_limit_window = 900  # 15 minutes in seconds
        self.max_requests_per_window = 100

        # Failed login attempts storage: {ip: [(timestamp, count)]}
        self.failed_login_storage = defaultdict(deque)
        self.login_attempt_window = 900  # 15 minutes in seconds
        self.max_login_attempts = 5

        # CSRF protection tokens
        self.csrf_tokens = set()

    async def __call__(self, request: Request, call_next: Callable[[Request], Awaitable[any]]):
        """
        Main security middleware function
        """
        # Get client IP
        client_ip = self.get_client_ip(request)

        # Check rate limiting
        if self.is_rate_limited(client_ip, request.url.path):
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": "Too many requests from this IP address"
                }
            )

        # Add security headers
        response = await call_next(request)
        self.add_security_headers(response)

        return response

    def get_client_ip(self, request: Request) -> str:
        """
        Get client IP address, considering proxy headers
        """
        forwarded = request.headers.get("x-forwarded-for")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.client.host

    def is_rate_limited(self, client_ip: str, endpoint: str) -> bool:
        """
        Check if the client is rate limited
        """
        current_time = time.time()

        # Clean old entries
        while (self.rate_limit_storage[client_ip] and
               self.rate_limit_storage[client_ip][0][0] < current_time - self.rate_limit_window):
            self.rate_limit_storage[client_ip].popleft()

        # Count requests in the current window
        request_count = len(self.rate_limit_storage[client_ip])

        # Add current request
        self.rate_limit_storage[client_ip].append((current_time, 1))

        return request_count >= self.max_requests_per_window

    def add_security_headers(self, response):
        """
        Add security headers to the response
        """
        # Prevent MIME type sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"

        # Prevent clickjacking
        response.headers["X-Frame-Options"] = "DENY"

        # Enable XSS protection
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # Content Security Policy
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self' https://api.example.com; "
            "frame-ancestors 'none';"
        )

        # Referrer Policy
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Feature Policy
        response.headers["Feature-Policy"] = (
            "geolocation 'none'; "
            "microphone 'none'; "
            "camera 'none';"
        )

        return response

    def check_failed_login_attempts(self, client_ip: str) -> bool:
        """
        Check if the IP has exceeded failed login attempts
        """
        current_time = time.time()

        # Clean old entries
        while (self.failed_login_storage[client_ip] and
               self.failed_login_storage[client_ip][0][0] < current_time - self.login_attempt_window):
            self.failed_login_storage[client_ip].popleft()

        # Count failed attempts in the current window
        failed_count = len(self.failed_login_storage[client_ip])

        return failed_count >= self.max_login_attempts

    def record_failed_login_attempt(self, client_ip: str):
        """
        Record a failed login attempt
        """
        current_time = time.time()
        self.failed_login_storage[client_ip].append((current_time, 1))

    def generate_csrf_token(self) -> str:
        """
        Generate a CSRF token
        """
        import secrets
        token = secrets.token_urlsafe(32)
        self.csrf_tokens.add(token)
        return token

    def validate_csrf_token(self, token: str) -> bool:
        """
        Validate a CSRF token
        """
        if token in self.csrf_tokens:
            self.csrf_tokens.remove(token)
            return True
        return False

# Initialize security middleware
security_middleware = SecurityMiddleware()

def get_security_middleware():
    return security_middleware

class InputSanitizer:
    """
    Input sanitization utilities
    """

    @staticmethod
    def sanitize_string(input_str: str, max_length: int = 1000) -> str:
        """
        Sanitize string input by removing dangerous characters
        """
        if not input_str:
            return input_str

        # Truncate to max length
        input_str = input_str[:max_length]

        # Remove potentially dangerous characters
        dangerous_chars = ['<', '>', '"', "'", '&', ';', '(', ')']
        for char in dangerous_chars:
            input_str = input_str.replace(char, '')

        return input_str.strip()

    @staticmethod
    def sanitize_html(input_html: str) -> str:
        """
        Sanitize HTML input by allowing only safe tags
        """
        from html import escape
        # For now, escape all HTML. In a real app, you'd use a library like bleach
        return escape(input_html)

    @staticmethod
    def validate_email_format(email: str) -> bool:
        """
        Validate email format using regex
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    @staticmethod
    def validate_url_format(url: str) -> bool:
        """
        Validate URL format
        """
        pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        return bool(re.match(pattern, url))

# Additional security utilities
class SecurityUtils:
    """
    Additional security utilities
    """

    @staticmethod
    def hash_password(password: str, salt: str = None) -> tuple:
        """
        Hash a password with salt
        """
        import hashlib
        import secrets

        if not salt:
            salt = secrets.token_hex(32)

        # Use SHA-256 with salt
        hashed = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
        return hashed.hex(), salt

    @staticmethod
    def verify_password(password: str, hashed: str, salt: str) -> bool:
        """
        Verify a password against its hash
        """
        import hashlib

        new_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
        return new_hash.hex() == hashed

    @staticmethod
    def generate_secure_token(length: int = 32) -> str:
        """
        Generate a cryptographically secure token
        """
        import secrets
        return secrets.token_urlsafe(length)