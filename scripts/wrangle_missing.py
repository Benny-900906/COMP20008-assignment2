"""
    code to handle all the schools with missing entries
"""

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

def get_sector_counts_dict(missing_final_csv=MISSING_FINAL_CSV):
    """
    counts up the sectors that each school is in,
    returns a dictionary of these
    """

    sector_counts = {}

    with open(missing_final_csv, 'r') as missing_final:
        lines = missing_final.readlines()
        entries = lines[0].split(',')

        sector_index = entries.index('Education Sector')

        for line in lines[1:]:
            entries = line.split(',')

            if entries[sector_index] not in sector_counts:
                sector_counts[entries[sector_index]] = 0
            sector_counts[entries[sector_index]] += 1
        
    return sector_counts

if __name__=='__main__':
    wrangle_missing()
    sector_counts = get_sector_counts_dict()

    print(sector_counts)