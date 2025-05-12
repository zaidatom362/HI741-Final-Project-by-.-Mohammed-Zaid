#!/usr/bin/env python3

# -*- coding: utf-8 -*-

"""

Utility Functions for the Clinical Data Warehouse


These helpers keep our code DRY and our data safe. 

Handles CSV reading/writing, logging, and other common chores.

"""


import csv

import os

from datetime import datetime


def load_csv_data(filename):

   """

   Read CSV data into a list of dictionaries.

   Returns an empty list if the file is missing or unreadable.


   Args:

       filename: Path to the CSV file.


   Returns:

       List of dicts, one per row. Empty list if file not found or unreadable.

   """

   try:

       with open(filename, 'r', newline='') as f:

           # Each row becomes a dictionary keyed by column name.

           return list(csv.DictReader(f))

   except FileNotFoundError:

       print(f"Warning: File {filename} not found. Returning empty list.")

       return []

   except PermissionError:

       print(f"Error: Can't open {filename} (permission denied).")

       return []

   except Exception as e:

       print(f"Error loading {filename}: {str(e)}")

       return []


def save_csv_data(filename, data, fieldnames=None):

   """

   Write a list of dictionaries to a CSV file, safely.

   Uses a temp file and atomic move to avoid data loss if something goes wrong.


   Args:

       filename: Where to save the CSV.

       data: List of dicts (rows).

       fieldnames: Optional list of column names. If not given, uses keys from the first row.

   """

   if not data:

       return # Nothing to write


   # Figure out the columns if not provided

   if not fieldnames and data:

       fieldnames = data[0].keys()


   # Make sure the folder exists

   os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)


   temp_file = f"{filename}.tmp"

   try:

       with open(temp_file, 'w', newline='') as f:

           writer = csv.DictWriter(f, fieldnames=fieldnames)

           writer.writeheader()

           writer.writerows(data)

       # Move the temp file into place (atomic replace)

       os.replace(temp_file, filename)

   except Exception as e:

       # If anything goes wrong, clean up the temp file

       if os.path.exists(temp_file):

           os.remove(temp_file)

       raise e


def log_activity(username, role, action):

   """

   Record what users are doing for audit trails and accountability.


   Args:

       username: Who did it.

       role: What hat they were wearing (admin, nurse, etc).

       action: What they did (e.g., 'Logged in', 'Viewed notes').

   """

   timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

   os.makedirs('data', exist_ok=True)

   log_file = 'data/usage_stats.csv'

   file_exists = os.path.exists(log_file)


   with open(log_file, 'a', newline='') as f:

       writer = csv.writer(f)

       # If this is a new file, write the header first

       if not file_exists or os.path.getsize(log_file) == 0:

           writer.writerow(['Timestamp', 'Username', 'Role', 'Action'])

       writer.writerow([timestamp, username, role, action])


def validate_date(date_str):

   """

   Check if a string looks like a date in YYYY-MM-DD format.


   Args:

       date_str: The date as a string.


   Returns:

       True if it's a valid date, False otherwise.

   """

   try:

       datetime.strptime(date_str, '%Y-%m-%d')

       return True

   except ValueError:

       return False


def generate_unique_id():

   """

   Make a unique ID for a new visit, patient, or whatever needs it.


   Returns:

       A string that's (almost) guaranteed to be unique.

   """

   import uuid

   return str(uuid.uuid4())


