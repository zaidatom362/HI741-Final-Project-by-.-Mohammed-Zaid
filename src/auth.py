#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Authentication Module - Handles user logins and access control
"""

from datetime import datetime
import csv
import os

class AuthSystem:
    """Manages user authentication and tracks login attempts."""

    def __init__(self, credentials_file='data/credentials.csv'):
        self.credentials_file = credentials_file
        self.credentials = self._load_credentials()  # Load users from CSV
        self.failed_attempts = {}  # Keeps count of failed logins per user

    def _load_credentials(self):
        # Reads the credentials CSV and builds a username lookup dictionary
        try:
            with open(self.credentials_file, 'r', newline='') as f:
                return {row['username']: row for row in csv.DictReader(f)}
        except FileNotFoundError:
            print("Warning: credentials.csv not found. No users loaded.")
            return {}

    def authenticate(self, username, password):
        # Check if the username exists in our records
        user = self.credentials.get(username)
        if not user:
            self._log(username, 'unknown', 'Failed: unknown user')
            return None

        # Check if the password matches
        if user['password'] != password:
            self._log(username, user['role'], 'Failed: wrong password')
            self.failed_attempts[username] = self.failed_attempts.get(username, 0) + 1
            return None

        # Successful login; reset failed attempts for this user
        if username in self.failed_attempts:
            del self.failed_attempts[username]

        self._log(username, user['role'], 'Successful login')
        return {
            'username': username,
            'role': user['role'],
            'login_time': datetime.now()
        }

    def _log(self, username, role, action):
        """Records login attempts and actions to usage_stats.csv"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        os.makedirs('data', exist_ok=True)  # Ensure the log directory exists

        log_file = 'data/usage_stats.csv'
        # Open log file in append mode
        with open(log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            # Write header if the file is empty
            if f.tell() == 0:
                writer.writerow(['Timestamp', 'Username', 'Role', 'Action'])
            writer.writerow([timestamp, username, role, action])
