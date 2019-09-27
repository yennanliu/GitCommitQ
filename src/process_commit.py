import pandas as pd 
from get_commit import Commit2df 

def load_df(csv_file):
    df = pd.read_csv(csv_file) 
    return df 

def get_user_id(df_col):
    return df_col['html_url']

def get_repo_url(df_col):
    return df_col.split('commit')[0]

def get_commit_timestamp(df_col):
    return df_col['author']['date']

def extract_inform(df):
    cols = ['user_id', 'commit_url', 'repo_url', 'commit_timestamp']
    result_df = pd.DataFrame()
    result_df['user_id'] = df['author'].map(get_user_id)
    result_df['commit_url'] = df['url']
    result_df['repo_url'] = df['html_url'].map(get_repo_url)
    result_df['commit_timestamp'] = df['commit'].map(get_commit_timestamp)
    print (result_df)
    return result_df

if __name__ == '__main__':
    repo_url = 'https://api.github.com/repos/apache/airflow/commits'
    print ('>>>> commit to df ...')
    df = Commit2df(repo_url)
    print ('>>>> extract from df ...')
    extract_inform(df)
