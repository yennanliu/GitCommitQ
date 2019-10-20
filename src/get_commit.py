import pandas as pd 
import json 
import requests

def Commit2df(url):
    """
    script transform scraped commit to pandas dataframe
    """
    print (url)
    response = requests.get(url)
    if response.status_code != 200:   # if there is no data, pass the scrapping process
        print ("""
               Not a valid response, repsone code : {}
               No commit data, return null dataframe
               """.format(response.status_code))
        return pd.DataFrame()
    # requests response -> text (python string) -> json 
    data_dict = json.loads(response.text)
    if len(data_dict) == 0:
        print ('Null scrapping data')
        return pd.DataFrame()
    df_cols = ['comments_url', 'node_id', 'commit', 'parents', 'url', 'author', 'sha', 'html_url', 'committer']
    collected = [ []  for i in range(len(df_cols))]
    for i in range(len(data_dict)):
        for index, col in enumerate(df_cols):
            collected[index].append(data_dict[i][col])
    # init dataframe 
    df = pd.DataFrame()
    for index, col in enumerate(df_cols):
        df[col] = collected[index]
    return df 
