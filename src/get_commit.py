from bs4 import BeautifulSoup
import pandas as pd 
import urllib 
import json 

def Commit2df(url):
    """
    script transform scraped commit to pandas dataframe
    """
    opener=urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    page = opener.open(url)
    soup = BeautifulSoup(page,"html.parser")
    # BeautifulSoup response -> text -> json 
    data_dict = json.loads(soup.getText())
    df_cols = list(data_dict[0].keys())
    collected = [ []  for i in range(len(df_cols))]
    for i in range(len(data_dict)):
        for index, col in enumerate(df_cols):
            collected[index].append(data_dict[i][col])
    # init dataframe 
    df = pd.DataFrame()
    for index, col in enumerate(df_cols):
        df[col] = collected[index]
    return df 
