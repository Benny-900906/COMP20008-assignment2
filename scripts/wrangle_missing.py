"""
    code to handle all the schools with missing entries
"""

import csv
import statistics

SCHOOL_FINAL_CSV = 'wrangled_df/school_final.csv'
MISSING_FINAL_CSV = 'wrangled_df/missing_school_final.csv'

def wrangle_missing(school_final_csv=SCHOOL_FINAL_CSV, missing_final_csv=MISSING_FINAL_CSV):
    """
    generates a file with just missing info
    """
    
    with open(school_final_csv, 'r') as school_final:
        with open(missing_final_csv, 'w') as missing_final:
            lines = school_final.readlines()
            missing_final.writelines(lines[0])
            missing_final.writelines([line for line in lines if line[-3:-1] == ',,'])

def get_sector_counts_dict(filename=MISSING_FINAL_CSV):
    """
    counts up the sectors that each school is in,
    returns a dictionary of these
    """

    sector_counts = {}

    with open(filename, 'r') as missing_final:
        missing_csv = csv.DictReader(missing_final)
        for row in missing_csv:
            if row['Education Sector'] not in sector_counts:
                sector_counts[row['Education Sector']] = 0
            sector_counts[row['Education Sector']] += 1
    
    return sector_counts

def get_median_income(filename=MISSING_FINAL_CSV):
    """
    gets the median income among schools
    """

    incomes = []
    with open(filename, 'r') as missing_final:
        missing_csv = csv.DictReader(missing_final)
        
        for row in missing_csv:
            if row['Median Income in Postcode'] != '':
                incomes.append(float(row['Median Income in Postcode']))

    return statistics.median(incomes)

if __name__=='__main__':
    wrangle_missing()
    sector_counts = get_sector_counts_dict()
    sector_counts_orig = get_sector_counts_dict(filename=SCHOOL_FINAL_CSV)
    median = get_median_income()
    median_orig = get_median_income(filename=SCHOOL_FINAL_CSV)

    print(sector_counts)
    print(median)
    print(sector_counts_orig)
    print(median_orig)