#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utility Functions Module for Clinical Data Warehouse
HI 741 Final Project
"""

import csv
import os
from datetime import datetime

def load_csv_data(filename):
    """
    Load data from CSV file with proper error handling.
    
    Args:
        filename: Path to the CSV file
        
    Returns:
        List of dictionaries representing CSV rows or empty list if file not found
    """
    try:
        with open(filename, 'r', newline='') as f:
            # Create list of dictionaries from CSV file
            return list(csv.DictReader(f))
    except FileNotFoundError:
        print(f"Warning: File {filename} not found. Returning empty list.")
        return []
    except PermissionError:
        print(f"Error: Permission denied when accessing {filename}.")
        return []
    except Exception as e:
        print(f"Error loading {filename}: {str(e)}")
        return []

def save_csv_data(filename, data, fieldnames=None):
    """
    Save data to CSV file using atomic write pattern for data integrity.
    
    Args:
        filename: Path to the CSV file
        data: List of dictionaries to save
        fieldnames: Optional list of field names for CSV header
    """
    if not data:
        return  # Don't write empty data
        
    # Get field names from first record if not provided
    if not fieldnames and data:
        fieldnames = data[0].keys()
        
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
        
    # Write to temporary file first (atomic write pattern)
    temp_file = f"{filename}.tmp"
    try:
        with open(temp_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
            
        # Atomically replace the original file
        os.replace(temp_file, filename)
    except Exception as e:
        # Clean up temp file if something went wrong
        if os.path.exists(temp_file):
            os.remove(temp_file)
        raise e

def log_activity(username, role, action):
    """
    Log user activity to usage_stats.csv for audit purposes.
    
    Args:
        username: Username of the user performing the action
        role: Role of the user (admin, management, nurse, clinician)
        action: Description of the action performed
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    log_file = 'data/usage_stats.csv'
    file_exists = os.path.exists(log_file)
    
    # Append to log file
    with open(log_file, 'a', newline='') as f:
        # Write header if file is new or empty
        if not file_exists or os.path.getsize(log_file) == 0:
            writer = csv.writer(f)
            writer.writerow(['Timestamp', 'Username', 'Role', 'Action'])
        
        writer = csv.writer(f)
        writer.writerow([timestamp, username, role, action])

def validate_date(date_str):
    """
    Validate date string format (YYYY-MM-DD).
    
    Args:
        date_str: Date string to validate
        
    Returns:
        True if valid, False otherwise
    """
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def generate_unique_id():
    """
    Generate a unique ID for visits or other records.
    
    Returns:
        String containing a unique identifier
    """
    import uuid
    return str(uuid.uuid4())
