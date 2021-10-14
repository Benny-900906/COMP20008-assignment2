"""
module for generating the heatmap
"""

import seaborn as sns
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

CSV_FILEPATH = '../final.csv'
VCE_HEATMAP_FILEPATH = 'vce_heatmap.png'

def generate_median_heatmap():
    csv_data = pd.read_csv(CSV_FILEPATH)
    vce_csv_data = csv_data[['Median Income in Postcode','VCE Median Study Score']]
    vce_valid_data = vce_csv_data.dropna()
    vce_valid_data = vce_valid_data.set_index('Median Income in Postcode')
    vce_valid_data = vce_valid_data.sort_index(ascending=True)
    sns.set(rc = {'figure.figsize':(2,10)})
    heatmap = sns.heatmap(vce_valid_data, annot=False, square=False, vmin=np.amin(vce_valid_data['VCE Median Study Score']), vmax=np.amax(vce_valid_data['VCE Median Study Score']), cmap='RdYlGn')
    plt.savefig(VCE_HEATMAP_FILEPATH, bbox_inches='tight')

if __name__ == "__main__":
    print("started")
    generate_median_heatmap()