
"""
Clinical Data Warehouse - Main Application
HI 741 Final Project
"""

import os
import sys
import argparse
from tkinter import messagebox

# Import modules with proper naming (no "update1" in names)
from src.auth import AuthSystem
from src.patients import PatientRegistry
from src.notes import NoteManager
from src.stats import StatsGenerator
from src.ui import ClinicalDataWarehouseUI

def parse_args():
    """Parse command line arguments for testing and automation"""
    parser = argparse.ArgumentParser(description="Clinical Data Warehouse Interface")
    parser.add_argument('-username', help='Username for direct login')
    parser.add_argument('-password', help='Password for direct login')
    return parser.parse_args()

def main():
    """Main application entry point"""
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)

    # Parse command line arguments
    args = parse_args()

    try:
        # Initialize core components
        auth_system = AuthSystem()
        patient_registry = PatientRegistry()
        note_manager = NoteManager()
        stats_generator = StatsGenerator(patient_registry)

        # Create and launch the UI
        app = ClinicalDataWarehouseUI(
            auth_system,
            patient_registry,
            note_manager,
            stats_generator
        )

        # Handle command-line login if provided (for testing)
        if args.username and args.password:
            app.username_var.set(args.username)
            app.password_var.set(args.password)
            app._login()

        # Start the application
        app.mainloop()

        return 0
    except Exception as e:
        # Handle unexpected errors gracefully
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
        print(f"ERROR: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
