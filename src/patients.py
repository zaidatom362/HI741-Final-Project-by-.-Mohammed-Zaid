#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PatientRegistry Module for Clinical Data Warehouse

Think of this as our hospital’s patient archive. It:
  • Loads existing visit records on startup  
  • Lets you look up a patient’s most recent visit  
  • Adds new visits with automatic IDs and timestamps  
  • Deletes all records for a given patient when needed  
  • Counts how many visits happened on any given day  
"""

import os
from datetime import datetime
from .utils import load_csv_data, save_csv_data, log_activity, generate_unique_id

class PatientRegistry:
    """
    Manages all patient visit records stored in Patient_data.csv.
    """

    def __init__(self, data_file='data/Patient_data.csv'):
        """
        On startup, load every visit into memory so we can work fast.
        
        data_file: path to the CSV holding historical visits
        """
        self.data_file = data_file
        # Each element is a dict representing one visit
        self.patients = load_csv_data(self.data_file)

    def get_patient(self, patient_id):
        """
        Find the most recent visit for this patient ID.
        Returns a dict of visit details, or None if we have no record.
        """
        # Gather all visits matching this ID
        visits = [p for p in self.patients if p.get('PatientID') == patient_id]
        if not visits:
            return None  # No visits found

        # Parse each visit’s date so we can pick the latest one
        for v in visits:
            v['_parsed_date'] = datetime.strptime(v['VisitDate'], '%Y-%m-%d')
        latest = max(visits, key=lambda v: v['_parsed_date'])
        # Clean up our helper field before returning
        del latest['_parsed_date']
        return latest

    def add_patient(self, patient_data, username):
        """
        Record a new patient visit.
        
        patient_data must include:
          PatientID, FirstName, LastName, Gender,
          DOB (YYYY-MM-DD), ChiefComplaint, Department
        
        We’ll stamp today’s date and generate a unique VisitID.
        Returns that new VisitID.
        """
        # Create the visit record
        visit_id = generate_unique_id()
        today = datetime.now().strftime('%Y-%m-%d')
        record = {
            'PatientID':      patient_data['PatientID'],
            'FirstName':      patient_data['FirstName'],
            'LastName':       patient_data['LastName'],
            'Gender':         patient_data['Gender'],
            'DOB':            patient_data['DOB'],
            'ChiefComplaint': patient_data['ChiefComplaint'],
            'Department':     patient_data['Department'],
            'VisitDate':      today,
            'VisitID':        visit_id
        }

        # Add to our in-memory list and save it back to CSV
        self.patients.append(record)
        save_csv_data(self.data_file, self.patients, fieldnames=list(record.keys()))

        # Log who added this record for auditing
        log_activity(username, 'patient_registry',
                     f"Added visit {visit_id} for Patient {record['PatientID']}")
        return visit_id

    def remove_patient(self, patient_id, username):
        """
        Wipe out every visit for this patient ID.
        Returns True if we deleted anything, False otherwise.
        """
        before = len(self.patients)
        # Keep only records that are NOT matching the ID
        self.patients = [
            p for p in self.patients
            if p.get('PatientID') != patient_id
        ]
        deleted = len(self.patients) < before
        if deleted:
            # Save the shortened list back to CSV
            keys = self.patients[0].keys() if self.patients else None
            save_csv_data(self.data_file, self.patients, fieldnames=keys)
            # Audit log the deletion event
            log_activity(username, 'patient_registry',
                         f"Removed all visits for Patient {patient_id}")
        return deleted

    def count_visits_by_date(self, date_str):
        """
        Count how many visits happened on a given date (YYYY-MM-DD).
        Simple tally from our in-memory list.
        """
        return sum(
            1 for p in self.patients
            if p.get('VisitDate') == date_str
        )

    def get_all_visits(self):
        """
        Give me a fresh list of every visit record.
        Handy for generating stats or reports.
        """
        return list(self.patients)
