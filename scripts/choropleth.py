"""
a massively simplified chloropleth drawing module
"""

import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd

DEFAULT_JSON = 'raw_data/3_postcode_polygon.json'
DEFAULT_CSV  = 'final.csv'
TAXATION_CSV = 'raw_data/0_taxation_by_postcode.csv'
DEFAULT_PNG  = 'visualisations/choropleth/graph.png'

def draw_choropleth(
    feature_name,
    title,
    rows=[],
    geojson=DEFAULT_JSON,
    csv=    DEFAULT_CSV,
    png=    DEFAULT_PNG,
    cmap=   'plasma'):
    """
        draw a choropleth of a given feature
    """

    # import all the data
    geojson_df = gpd.read_file(geojson)
    csv_df = pd.read_csv(csv)
    csv_df['Postcode'] = pd.to_numeric(csv_df['Postcode'])
    geojson_df['POSTCODE'] = pd.to_numeric(geojson_df['POSTCODE'])
    csv_df[feature_name] = pd.to_numeric(csv_df[feature_name])
    merged_df = geojson_df.merge(csv_df, left_on=['POSTCODE'], right_on=['Postcode'])
    if rows!=[]:
        rows_df = pd.DataFrame({
            "Postcode": rows
        })
        merged_df = merged_df.merge(rows_df, how='inner', left_on=['Postcode'], right_on=['Postcode'])
    
    # time to draw
    fig, ax = plt.subplots(1, dpi=1000, figsize=(10,6))
    
    merged_df.plot(column=feature_name, cmap=cmap, linewidth=0, ax=ax, legend=True)
    
    ax.axis('off')
    plt.title(title)
    plt.savefig(png)

def get_melbourne_postcodes():
    """
    get a dataframe of all the Metropolitan Melbourne postcodes
    """
    melbourne_postcodes = []
    melbourne_postcodes.extend([i for i in range(3000, 3211)])
    melbourne_postcodes.extend([i for i in [3335, 3336, 3338, 3427, 3428, 3429, 3750, 3751, 3752, 3754, 3755, 3759, 3760, 3761]])
    melbourne_postcodes.extend([i for i in range(3765, 3775)])
    melbourne_postcodes.extend([i for i in range(3781, 3787)])
    melbourne_postcodes.extend([i for i in range(3788, 3815)])
    melbourne_postcodes.extend([i for i in range(3910, 3920)])
    melbourne_postcodes.extend([i for i in range(3926, 3944)])
    melbourne_postcodes.extend([i for i in range(3975, 3978)])
    melbourne_postcodes.extend([3980])

    return melbourne_postcodes


if __name__ == '__main__':
    draw_choropleth(
        'Median taxable income or loss',
        'Median income across postcodes in Victoria',
        csv=TAXATION_CSV,
        png='visualisations/choropleth/median_income.png')
    
    draw_choropleth(
        'Average taxable income or loss',
        'Average income across postcodes in Victoria',
        csv=TAXATION_CSV,
        png='visualisations/choropleth/average_income.png')

    melbourne_postcodes = get_melbourne_postcodes()
    draw_choropleth(
        'Number of individuals lodging an income tax return',
        'Population Distribution',
        csv=TAXATION_CSV,
        png='visualisations/choropleth/population.png',
        cmap='Reds',
        rows=melbourne_postcodes
    )