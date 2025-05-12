#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clinical Data Warehouse UI

Provides a simple, role-based interface for hospital staff.
Users log in, then see only the actions they’re allowed:
finding patients, adding or removing records, viewing notes,
counting visits, and generating statistics.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

class ClinicalDataWarehouseUI(tk.Tk):
    """Main application window managing login and user workflows."""

    ROLE_MENUS = {
        'admin': ['count_visits', 'exit'],
        'management': ['generate_stats', 'exit'],
        'nurse': [
            'find_patient', 'add_patient', 'remove_patient',
            'count_visits', 'view_notes', 'exit'
        ],
        'clinician': [
            'find_patient', 'add_patient', 'remove_patient',
            'count_visits', 'view_notes', 'exit'
        ]
    }

    def __init__(self, auth_system, patient_db, note_manager, stats_engine):
        """Store references and show the login screen first."""
        super().__init__()
        self.auth = auth_system
        self.patients = patient_db
        self.notes = note_manager
        self.stats = stats_engine
        self.current_user = None

        self.title("Clinical Data Warehouse")
        self.geometry("800x600")
        self._show_login()

    def _clear(self):
        """Remove all current widgets."""
        for widget in self.winfo_children():
            widget.destroy()

    def _show_login(self):
        """Ask for user credentials to start a session."""
        self._clear()
        frame = ttk.Frame(self, padding=20)
        frame.pack(expand=True)

        ttk.Label(frame, text="Please log in", font=("Arial", 18)).pack(pady=10)
        ttk.Label(frame, text="Username:").pack(anchor='w')
        self.username = ttk.Entry(frame, width=30)
        self.username.pack(pady=5)
        ttk.Label(frame, text="Password:").pack(anchor='w')
        self.password = ttk.Entry(frame, width=30, show="*")
        self.password.pack(pady=5)
        ttk.Button(frame, text="Login", command=self._login).pack(pady=15)

    def _login(self):
        """Validate credentials and proceed or show an error."""
        user = self.auth.authenticate(
            self.username.get().strip(),
            self.password.get()
        )
        if user:
            self.current_user = user
            self._show_main_menu()
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password")

    def _show_main_menu(self):
        """Display actions based on the logged-in user's role."""
        self._clear()
        frame = ttk.Frame(self, padding=20)
        frame.pack(expand=True, fill='both')

        role = self.current_user['role']
        welcome = f"Welcome {self.current_user['username']} ({role})"
        ttk.Label(frame, text=welcome, font=("Arial", 14)).pack(pady=10)

        for action in self.ROLE_MENUS.get(role, []):
            label = action.replace('_', ' ').title()
            ttk.Button(
                frame, text=label,
                command=lambda a=action: self._handle_action(a),
                width=30
            ).pack(pady=5)

    def _handle_action(self, action):
        """Route each menu choice to its handler."""
        {
            'exit': self.quit,
            'find_patient': self._dialog_find_patient,
            'add_patient': self._dialog_add_patient,
            'remove_patient': self._dialog_remove_patient,
            'count_visits': self._dialog_count_visits,
            'view_notes': self._dialog_view_notes,
            'generate_stats': self._show_stats
        }.get(action, lambda: None)()

    def _dialog_find_patient(self):
        """Prompt for a patient ID and display their record."""
        dlg = tk.Toplevel(self)
        dlg.title("Find Patient")
        dlg.geometry("350x150")
        frame = ttk.Frame(dlg, padding=15)
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Patient ID:").pack(anchor='w')
        pid = ttk.Entry(frame, width=25)
        pid.pack(pady=5)

        def search():
            pid_val = pid.get().strip()
            if not pid_val:
                messagebox.showerror("Missing ID", "Enter a Patient ID")
                return
            patient = self.patients.get_patient(pid_val)
            if patient:
                self._display_patient(patient)
                dlg.destroy()
            else:
                messagebox.showinfo("Not Found", f"No record for ID {pid_val}")

        ttk.Button(frame, text="Search", command=search).pack(pady=10)

    def _display_patient(self, patient):
        """Show patient details in a read-only text area."""
        win = tk.Toplevel(self)
        win.title(f"Patient {patient['PatientID']}")
        win.geometry("500x400")

        text = tk.Text(win, wrap='word')
        text.pack(fill='both', expand=True)
        for key, val in patient.items():
            text.insert('end', f"{key}: {val}\n")
        text.config(state='disabled')

    def _dialog_add_patient(self):
        """Collect new patient data via form fields."""
        dlg = tk.Toplevel(self)
        dlg.title("Add Patient")
        dlg.geometry("400x350")
        frm = ttk.Frame(dlg, padding=15)
        frm.pack(fill='both', expand=True)

        fields = {}
        labels = ["Patient ID", "First Name", "Last Name", "Gender",
                  "DOB (YYYY-MM-DD)", "Chief Complaint", "Department"]
        for label in labels:
            ttk.Label(frm, text=label + ":").pack(anchor='w')
            entry = ttk.Entry(frm, width=30)
            entry.pack(pady=3)
            fields[label] = entry

        def add():
            data = {
                'PatientID': fields["Patient ID"].get().strip(),
                'FirstName': fields["First Name"].get().strip(),
                'LastName': fields["Last Name"].get().strip(),
                'Gender': fields["Gender"].get().strip(),
                'DOB': fields["DOB (YYYY-MM-DD)"].get().strip(),
                'ChiefComplaint': fields["Chief Complaint"].get().strip(),
                'Department': fields["Department"].get().strip()
            }
            if not data['PatientID']:
                messagebox.showerror("Missing ID", "Patient ID is required")
                return
            try:
                visit_id = self.patients.add_patient(data, self.current_user['username'])
                messagebox.showinfo("Success", f"Added, visit ID {visit_id}")
                dlg.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(frm, text="Add Patient", command=add).pack(pady=10)

    def _dialog_remove_patient(self):
        """Prompt for a patient ID and remove their record."""
        dlg = tk.Toplevel(self)
        dlg.title("Remove Patient")
        dlg.geometry("350x150")
        frm = ttk.Frame(dlg, padding=15)
        frm.pack(fill='both', expand=True)

        ttk.Label(frm, text="Patient ID to remove:").pack(anchor='w')
        pid = ttk.Entry(frm, width=25)
        pid.pack(pady=5)

        def remove():
            pid_val = pid.get().strip()
            if not pid_val:
                messagebox.showerror("Missing ID", "Enter a Patient ID")
                return
            success = self.patients.remove_patient(pid_val, self.current_user['username'])
            if success:
                messagebox.showinfo("Removed", f"Patient {pid_val} removed")
                dlg.destroy()
            else:
                messagebox.showinfo("Not Found", f"No record for ID {pid_val}")

        ttk.Button(frm, text="Remove", command=remove).pack(pady=10)

    def _dialog_count_visits(self):
        """Ask for a date and show how many visits occurred."""
        dlg = tk.Toplevel(self)
        dlg.title("Count Visits")
        dlg.geometry("350x150")
        frm = ttk.Frame(dlg, padding=15)
        frm.pack(fill='both', expand=True)

        ttk.Label(frm, text="Date (YYYY-MM-DD):").pack(anchor='w')
        date_entry = ttk.Entry(frm, width=25)
        date_entry.pack(pady=5)

        def count():
            date_str = date_entry.get().strip()
            try:
                datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                messagebox.showerror("Bad Format", "Use YYYY-MM-DD")
                return
            total = self.patients.count_visits_by_date(date_str)
            messagebox.showinfo("Visit Count", f"Visits on {date_str}: {total}")
            dlg.destroy()

        ttk.Button(frm, text="Count", command=count).pack(pady=10)

    def _dialog_view_notes(self):
        """Prompt for patient ID and date to display clinical notes."""
        dlg = tk.Toplevel(self)
        dlg.title("View Notes")
        dlg.geometry("350x200")
        frm = ttk.Frame(dlg, padding=15)
        frm.pack(fill='both', expand=True)

        ttk.Label(frm, text="Patient ID:").pack(anchor='w')
        pid_entry = ttk.Entry(frm, width=25)
        pid_entry.pack(pady=5)
        ttk.Label(frm, text="Date (YYYY-MM-DD):").pack(anchor='w')
        date_entry = ttk.Entry(frm, width=25)
        date_entry.pack(pady=5)

        def view():
            pid_val = pid_entry.get().strip()
            date_str = date_entry.get().strip()
            notes = self.notes.get_notes_by_date(pid_val, date_str, self.current_user['username'])
            if not notes:
                messagebox.showinfo("No Notes", "No notes found")
            else:
                self._display_notes(notes, pid_val, date_str)
            dlg.destroy()

        ttk.Button(frm, text="View", command=view).pack(pady=10)

    def _display_notes(self, notes, patient_id, date_str):
        """Show clinical notes in a scrollable window."""
        win = tk.Toplevel(self)
        win.title(f"Notes for {patient_id} on {date_str}")
        win.geometry("600x400")
        txt = tk.Text(win, wrap='word')
        txt.pack(fill='both', expand=True)
        for note in notes:
            txt.insert('end', f"{note['VisitDate']}: {note['NoteText']}\n\n")
        txt.config(state='disabled')

    def _show_stats(self):
        """Generate and display a plot of visit trends."""
        fig = self.stats.plot_visit_trends()
        win = tk.Toplevel(self)
        win.title("Visit Trends")
        win.geometry("800x600")
        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

if __name__ == "__main__":
    from auth import AuthSystem
    from patients import PatientRegistry
    from notes import NoteManager
    from stats import StatsGenerator

    app = ClinicalDataWarehouseUI(
        AuthSystem(),
        PatientRegistry(),
        NoteManager(),
        StatsGenerator()
    )
    app.mainloop()
