#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Notes Manager - Handles patient diaries (clinical notes) 
"""

import csv
from datetime import datetime
import os

class NoteManager:
    """Keeps track of patient stories and helps find them later."""

    def __init__(self, notes_file='data/Notes.csv'):
        """Sets up our notebook. Loads existing stories from file."""
        self.notes_file = notes_file
        self.notes = self._load_notes()  # Load past entries

    def _load_notes(self):
        """Reads our notebook from file. Starts fresh if missing."""
        try:
            with open(self.notes_file, 'r', newline='') as f:
                return list(csv.DictReader(f))  # Convert CSV to list of dicts
        except FileNotFoundError:
            print(f"Psst! {self.notes_file} is hiding. Starting with empty notes.")
            return []
        except Exception as e:
            print(f"Whoops! Trouble reading notes: {e}")
            return []

    def get_notes_by_date(self, patient_id, date_str, username=None):
        """
        Finds notes for a patient on specific day. 
        Fixes the 'too many notes' bug by strict date matching!
        """
        # First, check the date makes sense
        try:
            datetime.strptime(date_str, '%Y-%m-%d')  # Y-M-D format check
        except ValueError:
            return {'error': 'Date must look like 2023-12-31'}

        matching_notes = []
        for note in self.notes:
            # Match both patient ID and full date (no partial matches!)
            is_right_patient = note.get('PatientID') == patient_id
            starts_with_date = note.get('VisitDate', '').startswith(date_str)
            
            if is_right_patient and starts_with_date:
                matching_notes.append(note)

        # Tell the logbook someone looked at these notes
        if username:
            self._log_activity(username, 
                              f"Peeked at {len(matching_notes)} notes for {patient_id} on {date_str}")

        return matching_notes or []  # Return empty list instead of None

    def _log_activity(self, username, action):
        """Jots down who did what in our secret diary (usage log)"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        os.makedirs('data', exist_ok=True)  # Create folder if needed

        log_file = 'data/usage_stats.csv'
        # Check if we're starting a new diary
        new_diary = not os.path.exists(log_file) or os.path.getsize(log_file) == 0

        with open(log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            if new_diary:
                writer.writerow(['When', 'Who', 'What'])  # Simple headers
            writer.writerow([timestamp, username, action])
