import pandas as pd
import html.parser
from numpy import arange
import nltk
from nltk.corpus import stopwords
import re

DEFAULT_INCOME_FILE = 'raw_data/0_taxation_by_postcode.csv'
DEFAULT_SCHOOL_PERFORMANCE_FILE = 'raw_data/1_school_vce_performance.csv'
DEFAULT_SCHOOL_LOCATIONS_FILE = 'raw_data/2_school_locations.csv'

DEFAULT_OUTPUT_FILE = 'final.csv'

def wrangle_income(income_file):
    """
        takes the taxation_by_postcode file,
        extracts all the meaningful data from it
    """

    # load in the data
    income_data = pd.read_csv(income_file, encoding = "ISO-8859-1")

    # put together all the income data into a dataframe
    income_dataframe = pd.DataFrame({
        "Postcode": income_data["Postcode"],
        "Average Income in Postcode": income_data["Average salary or wages"],
        "Median Income in Postcode": income_data["Median salary or wages"]
    })

    return income_dataframe

def wrangle_school_locations(school_locations_file):
    """
        takes the school_locations.csv file,
        extracts the meaningful data and returns a dataframe
    """

    # 
    # get the school locations and average income data
    school_data = pd.read_csv(DEFAULT_SCHOOL_LOCATIONS_FILE, encoding = "ISO-8859-1")


    # only consider secondary schools
    school_data = school_data.loc[school_data["School_Type"] == "Secondary"]
    # and extract the postcode
    school_postcode = [x.upper() for x in school_data["Postal_Town"]]
    
    school_location_dataframe = pd.DataFrame({
        "School Name": school_data["School_Name"],
        "Locality": school_data["Postal_Town"],
        "Postcode": school_data["Postal_Postcode"]
    })
    return school_location_dataframe

def wrangle_school_performance(school_performance_file):
    """
        takes the school_performance.html file,
        extracts the meaningful data from it
    """

    # get the stopwords
    stop_words = set(stopwords.words("english"))

    # load in the data
    school_performance = pd.read_csv(school_performance_file, encoding = "ISO-8859-1")

    school_performance_dataframe = pd.DataFrame({
        "School Name": school_performance["School Name"],
        "Locality": school_performance["Locality"],
        "VCE Median Study Score": school_performance["VCE median study score"],
        "Percentage of study scores of 40 and over": school_performance["Percentage of study scores of 40 and over"]
    })

    return school_performance_dataframe

if __name__ == '__main__':
    # import each of the separate datasets
    income_data = wrangle_income(DEFAULT_INCOME_FILE)
    school_locations_data = wrangle_school_locations(DEFAULT_SCHOOL_LOCATIONS_FILE)
    school_performance_data = wrangle_school_performance(DEFAULT_SCHOOL_PERFORMANCE_FILE)
    
    # merge it all and export
    final_data = school_locations_data.merge(income_data, how='left', on='Postcode', sort=True)
    final_data = final_data.merge(school_performance_data, how='left', on=['School Name', 'Locality'])
    final_data.to_csv(DEFAULT_OUTPUT_FILE, index=False)
