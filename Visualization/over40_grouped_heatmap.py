"""
module for generating the heatmap
"""

import seaborn as sns
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

CSV_FILEPATH = '../final.csv'
OVER40_HEATMAP_FILEPATH = 'over40_grouped_heatmap.png'
    
def generate_over40_heatmap():
    
    csv_data = pd.read_csv(CSV_FILEPATH)
    over40_csv_data = csv_data[['Median Income in Postcode','Percentage of study scores of 40 and over']]
    over40_valid_data = over40_csv_data.dropna()

    # Extract "Median Income in Postcode" series
    median_income_data = pd.Series(over40_valid_data['Median Income in Postcode'])

    # Calculate the quartiles of "Median Income in Postcode"
    index_percentile = over40_valid_data.quantile([0, 0.25, 0.5, 0.75, 1], 0)['Median Income in Postcode']
    #print(index_percentile)
    #print('\n')
    
    # Separate the Median Income in Postcode and divide it into groups according to the quartiles
    labels_array = []
    for i in index_percentile.index:
        if i < index_percentile.index.max():
            labels_array.append('{}-{}'.format(index_percentile[i], index_percentile[i+0.25]))
    cutted_series = pd.qcut(median_income_data, 4, labels = labels_array)
    
    cutted_series.name = 'Median Income Groups'
    
    # Merge the cutted_series with median_series
    merged_df = pd.merge(over40_valid_data, cutted_series,  right_index = True, left_index = True)
    merged_df = merged_df.sort_values('Median Income Groups')#.set_index('Median Income Groups')
    merged_df.drop('Median Income in Postcode', axis=1, inplace=True)

    # Create the index array to draw the seperation lines on heatmap
    indices_counts = merged_df['Median Income Groups'].value_counts().sort_index()
    index_array = []
    start = 0
    for i in range(len(indices_counts.values) -1): # One less than the length because there should be no line at the bottom
        index_array.append(start + indices_counts.values[i])
        start += indices_counts.values[i]

    merged_df.sort_values(['Median Income Groups', 'Percentage of study scores of 40 and over'], ascending = (True, False), inplace = True)   
    merged_df = merged_df.set_index('Median Income Groups')
    
     # Generate the actual heatmap
    sns.set(rc = {'figure.figsize':(2,10)})
    heatmap = sns.heatmap(merged_df, cmap='RdYlGn')
    heatmap.hlines([index_array], *heatmap.get_xlim(), linestyles = 'dashed', color="black")
    plt.savefig(OVER40_HEATMAP_FILEPATH, bbox_inches='tight')


if __name__ == "__main__":
    print("started")
    generate_over40_heatmap()