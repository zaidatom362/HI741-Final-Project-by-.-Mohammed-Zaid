
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utility Functions for Clinical Data Warehouse

Handles safe CSV I/O, audit logging, date validation, and unique ID generation.
"""

import csv
import os
from datetime import datetime
from uuid import uuid4

def load_csv_data(filename):
    """
    Read CSV file into a list of dicts.
    Returns an empty list if the file cannot be read.
    """
    try:
        with open(filename, 'r', newline='') as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        print(f"Warning: File {filename} not found. Returning empty list.")
        return []
    except PermissionError:
        print(f"Error: Permission denied accessing {filename}.")
        return []
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return []

def save_csv_data(filename, data, fieldnames=None):
    """
    Write a list of dicts to a CSV file using an atomic temp‐file pattern.
    """
    if not data:
        return

    if not fieldnames:
        fieldnames = list(data[0].keys())

    os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
    temp_file = filename + '.tmp'
    try:
        with open(temp_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        os.replace(temp_file, filename)
    except Exception:
        if os.path.exists(temp_file):
            os.remove(temp_file)
        raise

def log_activity(username, role, action):
    """
    Append a timestamped record of user actions to output/audit_log.csv.
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    os.makedirs('output', exist_ok=True)
    log_file = 'output/audit_log.csv'
    first_entry = not os.path.exists(log_file) or os.path.getsize(log_file) == 0

    with open(log_file, 'a', newline='') as f:
        writer = csv.writer(f)
        if first_entry:
            writer.writerow(['Timestamp', 'Username', 'Role', 'Action'])
        writer.writerow([timestamp, username, role, action])

def validate_date(date_str):
    """
    Validate that date_str follows YYYY-MM-DD format.
    Returns True if valid, False otherwise.
    """
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def generate_unique_id():
    """
    Generate a universally unique identifier (UUID4).
    """
    return str(uuid4())
