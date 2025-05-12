
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
StatsGenerator: compute and plot visit‐trend statistics for the Clinical Data Warehouse.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from .utils import save_csv_data

class StatsGenerator:
    """
    Generate and plot visit trends from patient visit data.
    """

    def __init__(self, patient_registry):
        """
        patient_registry: instance of PatientRegistry
        """
        self.patient_registry = patient_registry

    def plot_visit_trends(self, days=30):
        """
        Build a bar chart of daily visit counts for the past `days` days,
        save those counts to output/visit_stats.csv, and return the Matplotlib Figure.
        """
        # Load all visits from the registry (assumed to return list of dicts)
        visits = self.patient_registry.get_all_visits()
        df = pd.DataFrame(visits)
        df['VisitDate'] = pd.to_datetime(df['VisitDate'])

        # Filter for the last `days` days
        cutoff = datetime.now() - timedelta(days=days)
        recent = df[df['VisitDate'] >= cutoff]

        # Count visits per day
        visit_counts = recent.groupby(recent['VisitDate'].dt.date).size()

        # --- WRITE OUT CSV OF VISIT STATISTICS ---
        os.makedirs('output', exist_ok=True)
        stats_rows = [
            {'Date': date.strftime('%Y-%m-%d'), 'VisitCount': int(count)}
            for date, count in visit_counts.items()
        ]
        save_csv_data(
            'output/visit_stats.csv',
            stats_rows,
            fieldnames=['Date', 'VisitCount']
        )
        # ------------------------------------------

        # Plotting
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(
            [d.strftime('%Y-%m-%d') for d in visit_counts.index],
            visit_counts.values,
            color='skyblue'
        )
        ax.set_title(f"Visits in Last {days} Days")
        ax.set_xlabel("Date")
        ax.set_ylabel("Number of Visits")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        return fig
