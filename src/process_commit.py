import pandas as pd 
import datetime
import uuid 

def generate_id(x):
    """
    generate tip id from user id, since tip id not exists in orgin data  
    """
    return str(uuid.uuid4())

def get_user_id(df_col):
    """
    get committer github user id 
    """
    try:
        return df_col['html_url']
    except:
        return 'NOT_FOUND'

def get_repo_url(df_col):
    """
    get commit repo url 
    """
    try:
        return df_col.split('commit')[0]
    except:
        return 'NOT_FOUND'

def get_commit_timestamp(df_col):
    """
    transorm commit_timestamp to form "%Y-%m-%dT%H:%M:%SZ"
    """
    return datetime.datetime.strptime(df_col['author']['date'],"%Y-%m-%dT%H:%M:%SZ")

def extract_inform(df):
    """
    get output data as pandas dataframe 
    """
    if len(df) == 0: # if there is no data, pass the data transform process
        print ('Null data, pass data process')
        return df
    cols = ['user_id', 'commit_url', 'repo_url', 'commit_timestamp']
    result_df = pd.DataFrame()
    result_df['user_id'] = df['author'].map(get_user_id)
    result_df['commit_url'] = df['url']
    result_df['repo_url'] = df['html_url'].map(get_repo_url)
    result_df['commit_timestamp'] = df['commit'].map(get_commit_timestamp)
    # create commit_id as the table primary key 
    result_df['commit_id'] = result_df['user_id'].map(generate_id) 
    print (result_df)
    return result_df
