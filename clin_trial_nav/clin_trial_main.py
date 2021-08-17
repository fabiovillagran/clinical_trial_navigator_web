from textwrap import wrap
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import json
from pandas.io.json import json_normalize # tranform JSON file into a pandas dataframe

    
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
        
def build_study_table(url):
        
    ## convert the clinicaltrials.gov JSON response to a pandas dataframe
    
    result = requests.get(url).json()
    result_list = [result for result in result['StudyFieldsResponse']['StudyFields'] if result['OutcomeMeasureType']]     #loop through the list and identify ONLY studies with outcome measures reported 
    df_master = json_normalize(result_list[0])      # initialize dataframe using JSON result

    try:
        for study in result_list[1:]:        # concatenate each study to the dataframe to generate master dataframe
            df = json_normalize(study)
            df_master = pd.concat([df_master, df], axis=0, ignore_index=True)
    except:
        pass
                                                                # extract list entries, reformat data in these columns as strings
    try:                                            
        df_master['NCTId'] = [df_master['NCTId'][i][0] for i in range(len(df_master['NCTId'])) if len(df_master['NCTId'][i]) > 0]
    except:
        pass        
    try:
        df_master['BriefTitle'] = [df_master['BriefTitle'][i][0] for i in range(len(df_master['BriefTitle'])) if len(df_master['BriefTitle'][i]) > 0]
    except:
        pass       
    try:
        df_master['Condition'] = [df_master['Condition'][i][0] for i in range(len(df_master['Condition'])) if len(df_master['Condition'][i]) > 0]
    except:
        pass
    try:
        df_master['StudyType'] = [df_master['StudyType'][i][0] for i in range(len(df_master['StudyType'])) if len(df_master['StudyType'][i]) > 0]
    except:
        pass
    
    
    for i in range(len(df_master['Phase'])):                    # extract clinical trial phase(s)
        if df_master['Phase'][i]:
            if len(df_master['Phase'][i]) > 1:
                df_master['Phase'][i] = df_master['Phase'][i][0] + ', ' + df_master['Phase'][i][1]
            else:
                df_master['Phase'][i] = df_master['Phase'][i][0]
        else:
            df_master['Phase'][i] = 'Unknown'
    
    
    try:
        df_master['EnrollmentCount'] = [df_master['EnrollmentCount'][i][0] for i in range(len(df_master['EnrollmentCount'])) if len(df_master['EnrollmentCount'][i]) > 0]
    except:
        pass
    try:
        df_master['StartDate'] = [df_master['StartDate'][i][0] for i in range(len(df_master['StartDate'])) if len(df_master['StartDate'][i]) > 0]
    except:
        pass
    try:
        df_master['PrimaryCompletionDate'] = [df_master['PrimaryCompletionDate'][i][0] for i in range(len(df_master['PrimaryCompletionDate'])) if len(df_master['PrimaryCompletionDate'][i]) > 0]
    except:
        pass
    try:
        df_master['EligibilityCriteria'] = [df_master['EligibilityCriteria'][i][0] for i in range(len(df_master['EligibilityCriteria'])) if len(df_master['EligibilityCriteria'][i]) > 0]
    except:
        pass
    try:
        df_master['InterventionName'] = [df_master['InterventionName'][i][0] for i in range(len(df_master['InterventionName'])) if len(df_master['InterventionName'][i]) > 0]
    except:
        pass
    try:
        df_master['ArmGroupInterventionName'] = [df_master['ArmGroupInterventionName'][i][0] for i in range(len(df_master['ArmGroupInterventionName'])) if len(df_master['ArmGroupInterventionName'][i]) > 0]
    except:
        pass
    try:
        df_master['ArmGroupDescription'] = [df_master['ArmGroupDescription'][i][0] for i in range(len(df_master['ArmGroupDescription'])) if len(df_master['ArmGroupDescription'][i]) > 0]
    except:
        pass
    try:
        df_master['InterventionArmGroupLabel'] = [df_master['InterventionArmGroupLabel'][i][0] for i in range(len(df_master['InterventionArmGroupLabel'])) if len(df_master['InterventionArmGroupLabel'][i]) > 0]
    except:
        pass


    #df_master['StartDate'] = pd.to_datetime(df_master['StartDate'])
    #df_master['PrimaryCompletionDate'] = pd.to_datetime(df_master['PrimaryCompletionDate'])            # future version of this project will convert starting / ending date to datetime format, to calculate/analyze trial duration
    
    
    return df_master
    



def build_outcome_table(df_master):
    
    # initialize an outcomes_df from the first study within the query study table
    
    study_1_nctid = df_master['NCTId'][0] 
    
    entry = df_master[df_master['NCTId']==study_1_nctid].reset_index().drop(columns='index')      # build a single df entry for this NCT ID

    df_outcomes = pd.DataFrame(columns=entry.columns)

    try:                            
        measures_per_outcome = len(entry['OutcomeMeasurementValue'][0])//len(entry['OutcomeMeasureTitle'][0])
    except:
        measures_per_outcome = 1


    df_outcomes = extract_outcomes(entry, df_outcomes, measures_per_outcome)
    
    study_2_nctid = df_master['NCTId'][1] 
    entry_2 = df_master[df_master['NCTId']==study_2_nctid].reset_index().drop(columns='index')      # build a single df entry for this NCT ID

    df = extract_outcomes(entry_2, df_outcomes, measures_per_outcome)
    outcomes_df = pd.concat([df_outcomes, df], axis=0, ignore_index=False)
    
    for i in range(1, len(df_master)):                         # concatenate each study to the dataframe to generate master dataframe
        study_x_nctid = df_master['NCTId'][i]
        entry_x = df_master[df_master['NCTId']==study_x_nctid].reset_index().drop(columns='index')      # build a single df entry for this NCT ID
        df = extract_outcomes(entry_x, df_outcomes, measures_per_outcome)
        outcomes_df = pd.concat([outcomes_df, df], axis=0, ignore_index=False)
    
    outcomes_df = outcomes_df.reset_index().drop(columns='index')
    
    return outcomes_df



# class Study:



def extract_outcomes(entry, df_outcomes, measures_per_outcome):            #iterate thru all outcome measures, create a dataframe with all required info
    
    try:
        df_outcomes = df_outcomes.drop(columns=['Rank', 'BriefTitle', 'Condition', 'Phase', 'StudyType', 'InterventionName',
         'EnrollmentCount', 'StartDate', 'PrimaryCompletionDate', 'EligibilityCriteria', 'ArmGroupDescription'])
    except:
        pass
    
    for i, item in enumerate(entry['OutcomeMeasureType']):
            
        try:
            df_outcomes['OutcomeMeasureType'] = [item for item in entry['OutcomeMeasureType']][0]
        except:
            pass
        try:
            df_outcomes['OutcomeMeasureTitle'] = [item for item in entry['OutcomeMeasureTitle']][0]
        except:
            pass
        try:
            df_outcomes['OutcomeMeasureDescription'] = [item for item in entry['OutcomeMeasureDescription']][0]
        except:
            pass
        try:
            df_outcomes['OutcomeMeasureTimeFrame'] = [item for item in entry['OutcomeMeasureTimeFrame']][0]
        except:
            pass
        try:
            df_outcomes['OutcomeMeasureUnitOfMeasure'] = [item for item in entry['OutcomeMeasureUnitOfMeasure']][0]
        except:
            pass
        try:
            df_outcomes['ArmGroupInterventionName'] = [item for item in entry['ArmGroupInterventionName']][0]
        except:
            pass
        try:
            df_outcomes['InterventionArmGroupLabel'] = [item for item in entry['InterventionArmGroupLabel']][0]
        except:
            pass

    beginning = 0
    increment = measures_per_outcome               # maps correct number of outcome measures reported in the study, as multiple performance values may pertain to each endpoint (i.e. value for each intervention arm + placebo)
    
    for i in range(len(df_outcomes)):
        try:
            df_outcomes['OutcomeMeasurementValue'][i] = entry['OutcomeMeasurementValue'][0][beginning:beginning+increment]
            beginning += increment
        except:
            pass
        try:
            df_outcomes['InterventionArmGroupLabel'][i] = entry['InterventionArmGroupLabel'][0]
        except:
            pass
        try:
            df_outcomes['InterventionName'][i] = entry['InterventionName'][0]
        except:
            pass
        try:
            df_outcomes['ArmGroupInterventionName'][i] = entry['ArmGroupInterventionName'][0]
        except:
            pass
    
    df_outcomes['NCTId'] = [item for item in entry['NCTId']][0]
    df_outcomes['Phase'] = [item for item in entry['Phase']][0]
    df_outcomes['BriefTitle'] = [item for item in entry['BriefTitle']][0]
    
    return df_outcomes

    

