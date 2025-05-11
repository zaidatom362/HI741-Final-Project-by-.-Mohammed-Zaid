#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Statistics Generation Module
"""

import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
import os

class StatsGenerator:
    """Generates statistics and visualizations from patient data"""

    def __init__(self, patient_registry):
        """Initialize with patient registry"""
        self.patient_registry = patient_registry

    def plot_visit_trends(self, days=30, output_file=None):
        """
        Generate plot for visit trends.
        This fixes the issue with just printing "1s" for dates.
        """
        # Convert patient data to pandas DataFrame for easier analysis
        df = pd.DataFrame(self.patient_registry.patients)

        if len(df) == 0 or 'VisitDate' not in df.columns:
            # Create empty plot if no data
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.set_title("No visit data available")
            ax.text(0.5, 0.5, "No patient visit data available",
                   horizontalalignment='center', verticalalignment='center')
            return fig

        # Convert strings to datetime
        df['VisitDate'] = pd.to_datetime(df['VisitDate'])

        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        # Filter data to date range
        mask = (df['VisitDate'] >= start_date) & (df['VisitDate'] <= end_date)
        filtered_df = df.loc[mask]

        # Group by date and count visits
        # This fixes the "1s" issue mentioned in feedback
        visit_counts = filtered_df.groupby(filtered_df['VisitDate'].dt.date).size()

        # Create bar plot with improved styling
        fig, ax = plt.subplots(figsize=(12, 6))
        visit_counts.plot(kind='bar', ax=ax, color='skyblue')

        # Add data labels on top of bars
        for i, count in enumerate(visit_counts):
            ax.text(i, count + 0.1, str(count), ha='center')

        # Customize plot
        ax.set_title(f"Patient Visits (Last {days} Days)")
        ax.set_xlabel("Date")
        ax.set_ylabel("Number of Visits")
        ax.tick_params(axis='x', rotation=45)
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()

        # Save to file if requested
        if output_file:
            plt.savefig(output_file, dpi=300)

        return fig
