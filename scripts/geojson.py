"""
module for wrangling the GeoJSON files,
turning them into a useful visualisation format
"""

import json
import matplotlib.pyplot as plt
from descartes import PolygonPatch

# define the colour blue
BLUE = '#6699cc'

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

    for postcode in postcode_to_polygon:
        print(postcode)

    return postcode_to_polygon

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


if __name__ == '__main__':
    postcode_to_polygon = get_postcode_to_polygon()
    draw_polygon('3056', postcode_to_polygon, 'visualisations/chloropleth/brunswick.png')
    draw_all_polygons(postcode_to_polygon, 'visualisations/chloropleth/vic.png')
    
