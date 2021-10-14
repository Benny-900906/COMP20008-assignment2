"""
module for generating the heatmap
"""

import seaborn as sns
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

CSV_FILEPATH = '../final.csv'
OVER40_HEATMAP_FILEPATH = 'over40_heatmap.png'
    
def generate_over40_heatmap():
    csv_data = pd.read_csv(CSV_FILEPATH)
    over40_csv_data = csv_data[['Median Income in Postcode','Percentage of study scores of 40 and over']]
    over40_valid_data = over40_csv_data.dropna()
    over40_valid_data = over40_valid_data.set_index('Median Income in Postcode')
    over40_valid_data = over40_valid_data.sort_index(ascending=True)
    sns.set(rc = {'figure.figsize':(2,10)})
    heatmap = sns.heatmap(over40_valid_data, annot=False, linewidths=0.00005, square=False, vmin=np.amin(over40_valid_data['Percentage of study scores of 40 and over']), vmax=np.amax(over40_valid_data['Percentage of study scores of 40 and over']), cmap='RdYlGn')
    plt.savefig(OVER40_HEATMAP_FILEPATH, bbox_inches='tight')

if __name__ == "__main__":
    print("started")
    generate_over40_heatmap()