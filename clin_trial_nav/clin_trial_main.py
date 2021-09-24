from textwrap import wrap
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import json
from pandas import json_normalize # tranform JSON file into a pandas dataframe
import time
import re

    
# class Query:        # class to create a query from the clinicaltrials API that will house the list of clinical trials returned from the API, with detailed information for each
    
#     def __init__(self, name = 'Query_1'):
#         self.name = name
#         self.study_tracker = []         # build list that tracks which studies have been built via build_study within the query

def build_url_from_query(query):
    
    query_tokenized = query.split()
    
    field_values = ['NCTId', 'BriefTitle', 'Condition', 'Phase', 'StudyType',
                    'EnrollmentCount', 'StartDate', 'PrimaryCompletionDate', 'EligibilityCriteria', 'InterventionName', 
                    'ArmGroupInterventionName', 'ArmGroupDescription', 'InterventionArmGroupLabel', 'OutcomeMeasureType', 'OutcomeMeasureTitle',
                    'OutcomeMeasureDescription', 'OutcomeMeasureTimeFrame', 'OutcomeMeasurementValue', 'OutcomeMeasureUnitOfMeasure']
    
    max_rank = 1000             # max # of items returned by the API query (max for the clinicaltrials.gov API is 1000)
    
    
    url = 'https://clinicaltrials.gov/api/query/study_fields?expr='
    
    for i, word in enumerate(query_tokenized):              # build query URL by adding all search terms and field values to the query URL, following the appropriate format
        if i == 0:
            url = url + word
        else:
            url = url + '+' + word
        
    url = url + '&fields='
    
    for i, word in enumerate(field_values):
        if i == 0:
            url = url + word
        else:
            url = url + '%2C' + word
    
    url = url + '&min_rnk=1&max_rnk=' + str(max_rank) + '&fmt=json' 
    url = url.strip()
    
    # print('\n\nQuerying up to 1,000 trials from clinicaltrials.gov with the following url...\n\n'+url+'\n\n')
    
    return url

def clean_columns(df_master):
    for col in df_master.columns[1:]:    
        if not re.search('Outcome.*', col):
            if len(df_master[col][0]) == 1:                                            
                df_master[col] = df_master[col][0]
            elif len(df_master[col][0]) > 1:
                df_master[col] = ', '.join(df_master[col][0])
            else:
                df_master[col] = 'Unknown'    
    return df_master

def build_study_table(url):
        
    ## convert the clinicaltrials.gov JSON response to a pandas dataframe
    
    result = requests.get(url).json()
    
    result_list = [result for result in result['StudyFieldsResponse']['StudyFields'] if result['OutcomeMeasureType']]     
    #loop through the list and identify ONLY studies with outcome measures reported 
    
    df_master = json_normalize(result_list[0])      # initialize dataframe using JSON result

    df_master = clean_columns(df_master)

    try:
        for study in result_list[1:]:        # concatenate each study to the dataframe to generate master dataframe
            df = json_normalize(study)
            df = clean_columns(df)
            df_master = pd.concat([df_master, df], axis=0, ignore_index=True)
    except:
        print("There was an error!")
        
    return df_master

def run_main():
    
    query_term = input("Enter search query: \n")
    start_time = time.process_time()
    url = build_url_from_query(query_term)
    print(f"Time to build url: {time.process_time()-start_time} seconds")
    
    start_time = time.process_time()
    study_table = build_study_table(url)
    print(f"Time to build table: {time.process_time()-start_time} seconds.")

    print(study_table)

# run_main()