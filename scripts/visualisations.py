"""
module for generating all the visualisations
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

DEFAULT_CSV = 'wrangled_df/final.csv'
DEFAULT_PNG = 'graph.png'

def scatter_plot(
        csv_filename=DEFAULT_CSV, 
        x_column='Average Income in Postcode ',
        x_label='Average Income in Postcode',
        x_min=40000, x_max=110000,
        y_column='VCE median study score',
        y_label='VCE Median Study Score',
        y_min=18, y_max=50,
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
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.savefig(png_filename)

if __name__ == "__main__":
    print("started")
    scatter_plot(png_filename='visualisations/income_vs_study_score.png')
    scatter_plot(
            y_label='Percentage of study scores of 40 and over',
            y_min=0, y_max=20,
            png_filename='visualisations/income_vs_over_40_scores.png')
