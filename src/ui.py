
"""
User Interface Module
"""

import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from datetime import datetime

class ClinicalDataWarehouseUI(tk.Tk):
    """Main UI class for the Clinical Data Warehouse"""

    # Role-based menu access
    ROLE_MENUS = {
        'admin': ['count_visits', 'exit'],
        'management': ['generate_stats', 'exit'],
        'nurse': ['retrieve_patient', 'add_patient', 'remove_patient',
                 'count_visits', 'view_note', 'exit'],
        'clinician': ['retrieve_patient', 'add_patient', 'remove_patient',
                     'count_visits', 'view_note', 'exit']
    }

    def __init__(self, auth_system, patient_registry, note_manager, stats_generator):
        """Initialize the UI with all required components"""
        super().__init__()

        # Store our dependencies
        self.auth = auth_system
        self.patients = patient_registry
        self.notes = note_manager
        self.stats = stats_generator

        # Set up the window
        self.title("Clinical Data Warehouse")
        self.geometry("800x600")
        self.current_user = None

        # Start with login screen
        self._show_login()

    def _show_login(self):
        """Display the login screen"""
        # Clear window
        for widget in self.winfo_children():
            widget.destroy()

        # Create login frame
        frame = ttk.Frame(self, padding=20)
        frame.pack(expand=True)

        # Title
        ttk.Label(frame, text="Clinical Data Warehouse",
                 font=("Arial", 18)).pack(pady=20)

        # Username
        ttk.Label(frame, text="Username:").pack(anchor='w')
        self.username_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.username_var, width=30).pack(pady=5)

        # Password
        ttk.Label(frame, text="Password:").pack(anchor='w')
        self.password_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.password_var, show="*", width=30).pack(pady=5)

        # Login button
        ttk.Button(frame, text="Login", command=self._login).pack(pady=20)

    def _login(self):
        """Handle login button click"""
        # Get credentials
        username = self.username_var.get()
        password = self.password_var.get()

        # Authenticate
        user = self.auth.authenticate(username, password)
        if user:
            self.current_user = user
            self._show_main_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def _show_main_menu(self):
        """Display the main menu based on user role"""
        # Clear window
        for widget in self.winfo_children():
            widget.destroy()

        # Get role
        role = self.current_user['role']

        # Create menu frame
        frame = ttk.Frame(self, padding=20)
        frame.pack(expand=True, fill='both')

        # Header
        ttk.Label(frame,
                 text=f"Welcome, {self.current_user['username']} ({role})",
                 font=("Arial", 14)).pack(pady=20)

        # Create buttons based on role
        for action in self.ROLE_MENUS.get(role, []):
            # Format action name
            action_name = ' '.join(word.capitalize() for word in action.split('_'))

            # Create button
            ttk.Button(
                frame,
                text=action_name,
                command=lambda a=action: self._handle_action(a),
                width=30
            ).pack(pady=5)

    def _handle_action(self, action):
        """Handle menu actions based on selection"""
        if action == 'exit':
            self.quit()
        elif action == 'retrieve_patient':
            self._show_retrieve_patient()
        elif action == 'add_patient':
            self._show_add_patient()
        elif action == 'remove_patient':
            self._show_remove_patient()
        elif action == 'count_visits':
            self._show_count_visits()
        elif action == 'view_note':
            self._show_view_note()
        elif action == 'generate_stats':
            self._show_stats()

    def _show_retrieve_patient(self):
        """Show dialog for retrieving patient information"""
        dialog = tk.Toplevel(self)
        dialog.title("Retrieve Patient")
        dialog.geometry("400x200")
        dialog.transient(self)

        frame = ttk.Frame(dialog, padding=20)
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Patient ID:").pack(anchor='w')
        patient_id_var = tk.StringVar()
        ttk.Entry(frame, textvariable=patient_id_var, width=30).pack(pady=5)

        def on_retrieve():
            patient_id = patient_id_var.get()
            if not patient_id:
                messagebox.showerror("Input Error", "Please enter a Patient ID")
                return

            patient = self.patients.get_patient(patient_id)
            if patient:
                self._display_patient(patient)
                dialog.destroy()
            else:
                messagebox.showinfo("Not Found", f"No patient found with ID {patient_id}")

        ttk.Button(frame, text="Retrieve", command=on_retrieve).pack(pady=20)

    def _display_patient(self, patient):
        """Display patient information in a new window"""
        window = tk.Toplevel(self)
        window.title(f"Patient: {patient['PatientID']}")
        window.geometry("600x400")

        frame = ttk.Frame(window, padding=20)
        frame.pack(fill='both', expand=True)

        # Create scrollable text area
        text = tk.Text(frame, wrap='word', height=20, width=70)
        text.pack(fill='both', expand=True)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame, command=text.yview)
        scrollbar.pack(side='right', fill='y')
        text.config(yscrollcommand=scrollbar.set)

        # Insert patient information
        text.insert('1.0', f"Patient ID: {patient['PatientID']}\n")
        for key, value in patient.items():
            if key != 'PatientID':
                text.insert('end', f"{key}: {value}\n")

        text.config(state='disabled')  # Make read-only

    def _show_add_patient(self):
        """Show dialog for adding a new patient"""
        dialog = tk.Toplevel(self)
        dialog.title("Add Patient")
        dialog.geometry("500x600")
        dialog.transient(self)

        frame = ttk.Frame(dialog, padding=20)
        frame.pack(fill='both', expand=True)

        # Patient ID
        ttk.Label(frame, text="Patient ID:").pack(anchor='w')
        patient_id_var = tk.StringVar()
        ttk.Entry(frame, textvariable=patient_id_var, width=30).pack(pady=5)

        # First Name
        ttk.Label(frame, text="First Name:").pack(anchor='w')
        first_name_var = tk.StringVar()
        ttk.Entry(frame, textvariable=first_name_var, width=30).pack(pady=5)

        # Last Name
        ttk.Label(frame, text="Last Name:").pack(anchor='w')
        last_name_var = tk.StringVar()
        ttk.Entry(frame, textvariable=last_name_var, width=30).pack(pady=5)

        # Gender
        ttk.Label(frame, text="Gender:").pack(anchor='w')
        gender_var = tk.StringVar()
        gender_combo = ttk.Combobox(frame, textvariable=gender_var, width=30)
        gender_combo['values'] = ('Male', 'Female', 'Other')
        gender_combo.pack(pady=5)

        # DOB
        ttk.Label(frame, text="Date of Birth (YYYY-MM-DD):").pack(anchor='w')
        dob_var = tk.StringVar()
        ttk.Entry(frame, textvariable=dob_var, width=30).pack(pady=5)

        # Chief Complaint
        ttk.Label(frame, text="Chief Complaint:").pack(anchor='w')
        complaint_var = tk.StringVar()
        ttk.Entry(frame, textvariable=complaint_var, width=30).pack(pady=5)

        # Department
        ttk.Label(frame, text="Department:").pack(anchor='w')
        department_var = tk.StringVar()
        department_combo = ttk.Combobox(frame, textvariable=department_var, width=30)
        department_combo['values'] = ('Emergency', 'Cardiology', 'Neurology', 'Oncology', 'Pediatrics', 'Other')
        department_combo.pack(pady=5)

        def on_add():
            # Validate required fields
            patient_id = patient_id_var.get()
            if not patient_id:
                messagebox.showerror("Input Error", "Patient ID is required")
                return

            # Create patient data dictionary
            patient_data = {
                'PatientID': patient_id,
                'FirstName': first_name_var.get(),
                'LastName': last_name_var.get(),
                'Gender': gender_var.get(),
                'DOB': dob_var.get(),
                'ChiefComplaint': complaint_var.get(),
                'Department': department_var.get()
            }

            # Add patient
            try:
                visit_id = self.patients.add_patient(patient_data, self.current_user['username'])
                messagebox.showinfo("Success", f"Patient added with Visit ID: {visit_id}")
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add patient: {str(e)}")

        ttk.Button(frame, text="Add Patient", command=on_add).pack(pady=20)

    def _show_remove_patient(self):
        """Show dialog for removing a patient"""
        dialog = tk.Toplevel(self)
        dialog.title("Remove Patient")
        dialog.geometry("400x200")
        dialog.transient(self)

        frame = ttk.Frame(dialog, padding=20)
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Patient ID:").pack(anchor='w')
        patient_id_var = tk.StringVar()
        ttk.Entry(frame, textvariable=patient_id_var, width=30).pack(pady=5)

        def on_remove():
            patient_id = patient_id_var.get()
            if not patient_id:
                messagebox.showerror("Input Error", "Please enter a Patient ID")
                return

            # Confirm removal
            confirm = messagebox.askyesno("Confirm", f"Are you sure you want to remove patient {patient_id}?")
            if not confirm:
                return

            success = self.patients.remove_patient(patient_id, self.current_user['username'])
            if success:
                messagebox.showinfo("Success", f"Patient {patient_id} removed")
                dialog.destroy()
            else:
                messagebox.showinfo("Not Found", f"No patient found with ID {patient_id}")

        ttk.Button(frame, text="Remove Patient", command=on_remove).pack(pady=20)

    def _show_count_visits(self):
        """Show dialog for counting visits on a specific date"""
        dialog = tk.Toplevel(self)
        dialog.title("Count Visits")
        dialog.geometry("400x200")
        dialog.transient(self)

        frame = ttk.Frame(dialog, padding=20)
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Date (YYYY-MM-DD):").pack(anchor='w')
        date_var = tk.StringVar()
        ttk.Entry(frame, textvariable=date_var, width=30).pack(pady=5)

        def on_count():
            date = date_var.get()
            if not date:
                messagebox.showerror("Input Error", "Please enter a date")
                return

            try:
                datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                messagebox.showerror("Input Error", "Invalid date format. Use YYYY-MM-DD")
                return

            count = self.patients.count_visits_by_date(date)
            messagebox.showinfo("Visit Count", f"Number of visits on {date}: {count}")

        ttk.Button(frame, text="Count Visits", command=on_count).pack(pady=20)

    def _show_view_note(self):
        """Show dialog for viewing patient notes"""
        dialog = tk.Toplevel(self)
        dialog.title("View Clinical Notes")
        dialog.geometry("400x200")
        dialog.transient(self)

        frame = ttk.Frame(dialog, padding=20)
        frame.pack(fill='both', expand=True)

        # Patient ID field
        ttk.Label(frame, text="Patient ID:").pack(anchor='w')
        patient_id_var = tk.StringVar()
        ttk.Entry(frame, textvariable=patient_id_var, width=30).pack(pady=5)

        # Date field
        ttk.Label(frame, text="Visit Date (YYYY-MM-DD):").pack(anchor='w')
        date_var = tk.StringVar()
        ttk.Entry(frame, textvariable=date_var, width=30).pack(pady=5)

        def on_view():
            patient_id = patient_id_var.get()
            date = date_var.get()

            if not patient_id or not date:
                messagebox.showerror("Input Error", "Please enter both Patient ID and Date")
                return

            # Use fixed note retrieval function
            notes = self.notes.get_notes_by_date(
                patient_id,
                date,
                self.current_user['username']
            )

            if isinstance(notes, dict) and 'error' in notes:
                messagebox.showerror("Error", notes['error'])
                return

            if not notes:
                messagebox.showinfo("No Notes", f"No notes found for patient {patient_id} on {date}")
                return

            # Display notes
            self._display_notes(notes, patient_id, date)
            dialog.destroy()

        ttk.Button(frame, text="View Notes", command=on_view).pack(pady=20)

    def _display_notes(self, notes, patient_id, date):
        """Display notes in a new window"""
        notes_window = tk.Toplevel(self)
        notes_window.title(f"Notes for {patient_id} on {date}")
        notes_window.geometry("800x600")

        frame = ttk.Frame(notes_window, padding=20)
        frame.pack(fill='both', expand=True)

        # Show number of notes
        ttk.Label(
            frame,
            text=f"Found {len(notes)} note(s)",
            font=("Arial", 12)
        ).pack(pady=10)

        # Create notebook if multiple notes
        if len(notes) > 1:
            notebook = ttk.Notebook(frame)
            notebook.pack(fill='both', expand=True)

            # Add tab for each note
            for i, note in enumerate(notes):
                note_frame = ttk.Frame(notebook, padding=10)
                notebook.add(note_frame, text=f"Note {i+1}")

                # Add text area
                text = tk.Text(note_frame, wrap='word')
                text.pack(fill='both', expand=True)

                # Add scrollbar
                scrollbar = ttk.Scrollbar(note_frame, command=text.yview)
                scrollbar.pack(side='right', fill='y')
                text.config(yscrollcommand=scrollbar.set)

                # Insert note text
                text.insert('1.0', note.get('NoteText', 'No text available'))
                text.config(state='disabled')  # Read-only
        else:
            # Just one note, show directly
            note = notes[0]

            # Add text area
            text = tk.Text(frame, wrap='word')
            text.pack(fill='both', expand=True)

            # Add scrollbar
            scrollbar = ttk.Scrollbar(frame, command=text.yview)
            scrollbar.pack(side='right', fill='y')
            text.config(yscrollcommand=scrollbar.set)

            # Insert note text
            text.insert('1.0', note.get('NoteText', 'No text available'))
            text.config(state='disabled')  # Read-only

    def _show_stats(self):
        """Show statistics visualization"""
        # Generate plot
        fig = self.stats.plot_visit_trends()

        # Create window
        stats_window = tk.Toplevel(self)
        stats_window.title("Visit Statistics")
        stats_window.geometry("1000x600")

        # Create frame
        frame = ttk.Frame(stats_window, padding=10)
        frame.pack(fill='both', expand=True)

        # Embed plot
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

        # Add toolbar
        from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
        toolbar = NavigationToolbar2Tk(canvas, frame)
        toolbar.update()
