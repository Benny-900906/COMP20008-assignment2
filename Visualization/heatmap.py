"""
module for generating the heatmap
"""

import seaborn as sns
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

CSV_FILEPATH = '../final.csv'
HEATMAP_FILEPATH = 'heatmap.png'

def generate_heatmap():
    csv_data = pd.read_csv(CSV_FILEPATH)
    csv_data = csv_data[['Median Income in Postcode','VCE Median Study Score']]
    valid_data = csv_data.dropna()
    valid_data = valid_data.set_index('Median Income in Postcode')
    valid_data = valid_data.sort_index(ascending=False)
    print(valid_data)
    heatmap = sns.heatmap(valid_data, annot=False, linewidths=0.00005, square=False, vmin=np.amin(valid_data['VCE Median Study Score']), vmax=np.amax(valid_data['VCE Median Study Score']), cmap='RdYlGn')
    plt.savefig(HEATMAP_FILEPATH, bbox_inches='tight')
    
if __name__ == "__main__":
    print("started")
    generate_heatmap()