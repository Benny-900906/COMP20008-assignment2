"""
module for wrangling the GeoJSON files,
turning them into a useful visualisation format
"""

import json
import matplotlib.pyplot as plt
from descartes import PolygonPatch
import pandas as pd
from csv import reader
from colorutils import Color
import geopandas as gpd

# define the colour blue
BLUE = '#6699cc'

# default file locations
DEFAULT_CSV = 'raw_data/0_taxation_by_postcode.csv'
DEFAULT_JSON = 'raw_data/3_postcode_polygon.json'

def get_features_from_json(filename):
    """
        takes a filename,
        extracts JSON data and returns the features of the data
    """

    data = {}
    with open(filename) as file:
        text = file.read()
        data = json.loads(text)

    return data["features"]

def get_postcode_to_polygon():
    """
        produces a dictionary that converts postcodes to polygons
    """

    postcode_to_polygon = {}

    features = get_features_from_json(DEFAULT_JSON)
    for feature in features:
        postcode = feature["properties"]["POSTCODE"]
        polygon = feature["geometry"]
        postcode_to_polygon[postcode] = polygon

    return postcode_to_polygon


def get_postcode_to_color(postcode_to_feature, min_hue=0, max_hue=200):
    """
        create a dictionary converting color
    """

    postcode_to_hex = {}
    
    values = [float(val) for val in postcode_to_feature.values() if val != '']
    min_val = min(values)
    max_val = max(values)
    val_range = max_val - min_val
    hue_range = max_hue - min_hue

    for postcode in postcode_to_feature:
        if postcode_to_feature[postcode] == '':
            continue

        value = float(postcode_to_feature[postcode])
        hue = (((value - min_val) * hue_range) / val_range) + min_hue
        # print(f'calculated {hue}')
        color = Color(hsv=(hue, 1, 1)).hex
        # color = Color(hsv=(hue, 255, 255)).hex

        postcode_to_hex[postcode] = color

    return postcode_to_hex


def get_postcode_to_feature(filename, feature):
    """
        open a csv,
        and get a dictionary converting postcodes to a certain value
    """

    postcode_to_feature = {}

    with open(filename, 'r') as file:
        lines = file.readlines()

        headers = lines[0].split(',')
        postcode_index = headers.index('Postcode')
        feature_index  = headers.index(feature)

        for line in lines[1:]:
            values = line.split(',')
            postcode_to_feature[values[postcode_index]] = values[feature_index]
    
    return postcode_to_feature


def draw_polygon(postcode, postcode_to_polygon, filename):
    """
        takes a postcode and the postcode_to_polygon dictionary,
        produces a drawing of the polygon at that postcode
    """

    poly = postcode_to_polygon[postcode]
    fig = plt.figure()
    ax = fig.gca()
    ax.add_patch(PolygonPatch(poly, fc=BLUE, ec=BLUE, alpha=0.5, zorder=2))
    ax.axis('scaled')
    plt.savefig(filename)


def draw_all_polygons(postcode_to_polygon, filename):
    """
        draws every single entry in postcode_to_polygon
    """
    
    # set up the figure
    fig = plt.figure()
    ax = fig.gca()

    # add every postcode to the figure
    for postcode in postcode_to_polygon:
        poly = postcode_to_polygon[postcode]
        ax.add_patch(PolygonPatch(poly, fc=BLUE, ec=BLUE, alpha=0.5, zorder=2))

    # scale and export
    ax.axis('scaled')
    plt.savefig(filename)



def draw_polygons_colored(postcodes, postcode_to_polygon, postcode_to_color, filename):
    """
        draws every polygon, colored in accordance with a postcode_to_color dict
    """
    print('drawing the polygons colored')

    # set up the figure
    fig = plt.figure(dpi=800)
    ax = fig.gca()

    # add every postcode to the figure
    for postcode in postcodes:
        if postcode not in postcode_to_polygon or postcode not in postcode_to_color:
            continue

        poly = postcode_to_polygon[postcode]
        color = postcode_to_color[postcode]
        ax.add_patch(PolygonPatch(poly, fc=color, ec=None, linewidth=0, alpha=1, zorder=2))

    # scale and export
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    
    ax.axis('scaled')
    plt.title('Median income across Victoria')
    plt.savefig(filename)


if __name__ == '__main__':
    postcode_to_polygon = get_postcode_to_polygon()
    postcode_to_income = get_postcode_to_feature(DEFAULT_CSV, "Median taxable income or loss")
    # print(postcode_to_income['3056'])
    # print(postcode_to_income)
    postcode_to_color = get_postcode_to_color(postcode_to_income)
    # print(postcode_to_color)

    melbourne_postcodes = []
    melbourne_postcodes.extend([str(i) for i in range(3000, 3211)])
    melbourne_postcodes.extend([str(i) for i in [3335, 3336, 3338, 3427, 3428, 3429, 3750, 3751, 3752, 3754, 3755, 3759, 3760, 3761]])
    melbourne_postcodes.extend([str(i) for i in range(3765, 3775)])
    melbourne_postcodes.extend([str(i) for i in range(3781, 3787)])
    melbourne_postcodes.extend([str(i) for i in range(3788, 3815)])
    melbourne_postcodes.extend([str(i) for i in range(3910, 3920)])
    melbourne_postcodes.extend([str(i) for i in range(3926, 3944)])
    melbourne_postcodes.extend([str(i) for i in range(3975, 3978)])
    melbourne_postcodes.extend([str(3980)])

    # print(melbourne_postcodes)
    # draw_polygon('3056', postcode_to_polygon, 'visualisations/chloropleth/brunswick.png')
    # draw_all_polygons(postcode_to_polygon, 'visualisations/chloropleth/vic.png')
    draw_polygons_colored(melbourne_postcodes, postcode_to_polygon, postcode_to_color, 'visualisations/choropleth/median_income2.png')
