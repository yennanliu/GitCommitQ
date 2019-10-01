import pandas as pd 
from datetime import datetime
import uuid 
# UDF  
from get_commit import Commit2df 

def generate_id(x):
    """
    generate tip id from user id, since tip id not exists in orgin data  
    """
    return str(uuid.uuid4())

def get_user_id(df_col):
    try:
        return df_col['html_url']
    except:
        return 'NOT_FOUND'

def get_repo_url(df_col):
    try:
        df_col.split('commit')[0]
    except:
        return 'NOT_FOUND'

def get_commit_timestamp(df_col):
    return datetime.strptime(df_col['author']['date'],"%Y-%m-%dT%H:%M:%SZ")

def extract_inform(df):
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
