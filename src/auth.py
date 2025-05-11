
"""
Authentication Module
"""

from datetime import datetime
import csv
import os

class AuthSystem:
    """Handles user authentication and role-based access control"""

    def __init__(self, credentials_file='data/credentials.csv'):
        """Initialize authentication system with credentials file"""
        self.credentials_file = credentials_file
        self.credentials = self._load_credentials()
        self.failed_attempts = {}  # Track failed login attempts

    def _load_credentials(self):
        """Load user credentials from CSV file"""
        try:
            with open(self.credentials_file, 'r', newline='') as f:
                # Create dictionary for O(1) lookup by username
                return {row['username']: row for row in csv.DictReader(f)}
        except FileNotFoundError:
            print(f"Warning: Credentials file {self.credentials_file} not found.")
            return {}

    def authenticate(self, username, password):
        """Authenticate user based on username and password"""
        # Look up the user in our credentials dictionary
        user = self.credentials.get(username)

        if not user:
            # Username not found - log the attempt
            self._log_activity(username, 'unknown', 'Failed login (user not found)')
            return None

        if user['password'] != password:
            # Password incorrect - log the attempt
            self._log_activity(username, user['role'], 'Failed login (incorrect password)')

            # Track failed attempts (could implement lockout for security)
            if username not in self.failed_attempts:
                self.failed_attempts[username] = 0
            self.failed_attempts[username] += 1

            return None

        # Successful login - reset failed attempts and log success
        if username in self.failed_attempts:
            del self.failed_attempts[username]

        self._log_activity(username, user['role'], 'Successful login')

        # Return user information
        return {
            'username': username,
            'role': user['role'],
            'login_time': datetime.now()
        }

    def _log_activity(self, username, role, action):
        """Log user activity to usage_stats.csv"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Ensure directory exists
        os.makedirs('data', exist_ok=True)

        log_file = 'data/usage_stats.csv'
        file_exists = os.path.exists(log_file)

        # Append to log file
        with open(log_file, 'a', newline='') as f:
            # Write header if file is new
            if not file_exists or os.path.getsize(log_file) == 0:
                writer = csv.writer(f)
                writer.writerow(['Timestamp', 'Username', 'Role', 'Action'])

            writer = csv.writer(f)
            writer.writerow([timestamp, username, role, action])
