#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clinical Data Warehouse Package

Imagine this as the reception desk for our hospital’s data system.
When you import this package, you get quick access to:

  • AuthSystem – handles staff logins  
  • PatientRegistry – keeps track of patient records  
  • NoteManager – looks up clinical notes  
  • StatsGenerator – creates visit trend charts  
  • ClinicalDataWarehouseUI – launches the Tkinter interface  
  • utils – helpers for CSV handling, logging, date checks, and IDs  

Just import whatever you need and get started.
"""

# Who gets in and what they can do
from .auth import AuthSystem

# Patient record storage and CRUD operations
from .patients import PatientRegistry

# Clinical notes loader and search tool
from .notes import NoteManager

# Visit statistics calculator and plotter
from .stats import StatsGenerator

# The main graphical interface for hospital staff
from .ui import ClinicalDataWarehouseUI

# Handy helper functions used all around the package
from .utils import (
    load_csv_data,    # read CSV files into lists of dicts
    save_csv_data,    # write lists of dicts back as CSV safely
    log_activity,     # record user actions for auditing
    validate_date,    # check that dates look like YYYY-MM-DD
    generate_unique_id  # create UUIDs for new records
)

# When you do `from datawarehouse import *`, here’s what you get
__all__ = [
    "AuthSystem",
    "PatientRegistry",
    "NoteManager",
    "StatsGenerator",
    "ClinicalDataWarehouseUI",
    "load_csv_data",
    "save_csv_data",
    "log_activity",
    "validate_date",
    "generate_unique_id",
]
