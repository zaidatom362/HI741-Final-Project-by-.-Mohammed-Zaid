# HI741-Final-Project-by-.-Mohammed-Zaid
# Clinical Data Warehouse

I built this desktop application so hospital staff can log in securely, manage patient records, view clinical notes, count visits, and generate visit‐trend charts. The UI adapts to each user’s role (admin, management, nurse, clinician), making it simple and safe.

## Description

I created a role‐based Tkinter interface that connects to CSV data files:

- **Credentials.csv** for user authentication  
- **Patient_data.csv** for patient demographics and visit history  
- **Notes.csv** for clinical note archives  

The app guides you through finding, adding, or removing patients; viewing notes; counting visits on a particular date; and plotting visit trends over time.

## Tech Stack

- **Python 3.9+**  
- **Tkinter** for the GUI  
- **Pandas** for CSV handling  
- **Matplotlib** for plotting  
- **Conda** or **pip** for environment management  

## Features

- **Secure Login** with role validation  
- **Role-Based Menus**: each role sees only its allowed actions  
- **Patient Management**: find by ID, add new, remove existing  
- **Clinical Notes**: look up notes by patient ID and date  
- **Visit Counter**: get daily visit totals (YYYY-MM-DD format)  
- **Trend Visualization**: bar charts of daily visits over a time window  
- **Audit Logging & Safe CSV Writes** via atomic file operations  

## Installation & Setup

1. **Clone the repo**  

git clone https://github.com/zaidatom362/HI741-Final-Project.git
cd HI741-Final-Project

2. **Create your environment**
conda create -n cdw-env python=3.9 pandas matplotlib
conda activate cdw-env


or

3. **Prepare CSV files** in `data/`:  
- `Credentials.csv`  
- `Patient_data.csv`  
- `Notes.csv`  

## How to Run

From the project root, type:

python main.py

HI741-Final-Project/
HI741-Final-Project/
├── data/
│   ├── Credentials.csv
│   ├── Notes.csv
│   └── Patient_data.csv
├── output/
│   ├── visit_trends.png
│   └── audit_log.csv
├── src/
│   ├── __init__.py
│   ├── auth.py
│   ├── patients.py
│   ├── notes.py
│   ├── stats.py
│   ├── ui.py
│   └── utils.py
├── main.py
├── requirements.txt
└── README.md

