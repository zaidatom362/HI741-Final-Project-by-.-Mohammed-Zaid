
"""
Clinical Notes Management Module
"""

import csv
from datetime import datetime
import os

class NoteManager:
    """Manages clinical notes and provides search functionality"""

    def __init__(self, notes_file='data/Notes.csv'):
        """Initialize note manager with notes file"""
        self.notes_file = notes_file
        self.notes = self._load_notes()

    def _load_notes(self):
        """Load clinical notes from CSV file"""
        try:
            with open(self.notes_file, 'r', newline='') as f:
                return list(csv.DictReader(f))
        except FileNotFoundError:
            print(f"Warning: Notes file {self.notes_file} not found.")
            return []

    def get_notes_by_date(self, patient_id, date_str, username=None):
        """
        Get notes for a patient on a specific date.
        This fixes the issue with showing too many notes!
        """
        # Validate date format
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            return {'error': 'Invalid date format. Use YYYY-MM-DD'}

        # Filter notes by patient ID and exact date match
        matching_notes = []
        for note in self.notes:
            # Check if both PatientID matches and date is exactly the same
            # This is the fix for showing too many notes!
            if (note['PatientID'] == patient_id and
                note['VisitDate'].startswith(date_str)):
                matching_notes.append(note)

        # Log this access
        if username:
            self._log_activity(username, f"Viewed notes for patient {patient_id} on {date_str}")

        return matching_notes

    def _log_activity(self, username, action):
        """Log note-related activity"""
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
                writer.writerow(['Timestamp', 'Username', 'Action'])

            writer = csv.writer(f)
            writer.writerow([timestamp, username, action])
