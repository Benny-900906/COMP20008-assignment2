"""
module for generating all the visualisations
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

DEFAULT_CSV = 'final.csv'
DEFAULT_PNG = 'visualisations/scatter/graph.png'

def scatter_plot(
        csv_filename=DEFAULT_CSV, 
        x_column='Median Income in Postcode',
        x_range=[30000, 70000],
        y_column='VCE Median Study Score',
        y_range=[18, 50],
        png_filename=DEFAULT_PNG):
    """
        take a CSV file and draw up a scatter plot from the relevant columns
    """

    # get the data
    csv_data = pd.read_csv(csv_filename)

    x_data = csv_data[x_column]
    y_data = csv_data[y_column]

    # graph it
    plt.figure()
    plt.scatter(x_data, y_data)
    plt.grid(True)
    plt.xlim(x_range[0], x_range[1])
    plt.ylim(y_range[0], y_range[1])
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.savefig(png_filename)

if __name__ == "__main__":
    print("started")
    scatter_plot(png_filename='visualisations/scatter/income_vs_study_score.png')
    scatter_plot(
            y_column='Percentage of study scores of 40 and over',
            y_range=[0,20],
            png_filename='visualisations/scatter/income_vs_over_40_scores.png')
