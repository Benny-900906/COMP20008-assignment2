"""
wrangles together a csv that focuses on school performance per postcode
(eg rather than showing the VCE performance of each school,
it shows the average VCE score in a postcode)

exports to wrangled_df/postcode_final.csv
(you need to run wrangle_schools.py FIRST!)
"""

import statistics

SCHOOL_DATA_FINAL_CSV = 'wrangled_df/school_final.csv'
POSTCODE_CSV = 'wrangled_df/postcode_final.csv'

class PostcodeData:
    """
    a class for storing all the data about each postcode
    """
    def __init__(self):
        self.postcode = None
        self.median_vce_study_score = None
        self.median_percentage_over_40 = None

    def to_csv(self):
        return f"{self.postcode},{self.median_vce_study_score},{self.median_percentage_over_40}\n"

def postcode_dict_to_csv(postcode_dict, filename):
    """
        convert a postcode dictionary to a csv file
    """

    with open(filename, 'w') as file:
        file.write('Postcode,Median VCE Study Score,Median Percentage of Study Scores over 40\n')
        for postcode in postcode_dict:
            file.write(postcode_dict[postcode].to_csv())

def produce_postcode_dict():
    postcode_dict = {}

    school_data_file = open(SCHOOL_DATA_FINAL_CSV, 'r')
    
    school_lines = school_data_file.readlines()
    school_header = school_lines[0].strip().split(',')

    print(school_header)
    vce_study_score_index = school_header.index('VCE Median Study Score')
    over_40_index = school_header.index('Percentage of study scores of 40 and over')
    postcode_index = school_header.index('Postcode')

    print(f"postcode index is {postcode_index}")

    postcode_to_study_scores = {}
    postcode_to_over_40 = {}
    

    for school_line in school_lines[1:]:
        print(school_line)
        entries = school_line.strip().split(',')
        
        to_float = lambda s : None if s == '' else float(s)

        postcode = int(entries[postcode_index])
        vce_study_score = to_float(entries[vce_study_score_index])
        over_40 = to_float(entries[over_40_index])

        # skip the ones that don't work
        if vce_study_score is None and over_40 is None:
            print(f'skipping {postcode} because there\'s no school data\n')
            continue

        if postcode not in postcode_to_study_scores:
            postcode_to_study_scores[postcode] = []
        print(f'appending vce score {vce_study_score} to {postcode}')
        postcode_to_study_scores[postcode].append(vce_study_score)

        if postcode not in postcode_to_over_40:
            postcode_to_over_40[postcode] = []
        # print(f'appending over_40 {over_40} to {postcode}')
        postcode_to_over_40[postcode].append(over_40)

    for postcode in postcode_to_study_scores:
        postcode_dict[postcode] = PostcodeData()
        postcode_dict[postcode].postcode = postcode
        postcode_dict[postcode].median_vce_study_score = statistics.median(postcode_to_study_scores[postcode])
        postcode_dict[postcode].median_percentage_over_40 = statistics.median(postcode_to_over_40[postcode])
        
    school_data_file.close()
    return postcode_dict

if __name__=='__main__':
    postcode_dict = produce_postcode_dict()
    postcode_dict_to_csv(postcode_dict, 'test.csv')