import sys
sys.path.append("./script/")
import datetime
import time
# UDF 
from utility import * 
from get_commit import *
from process_commit import *
from dump_to_postgre import * 

def daterange_2_datelist(start_date, end_date):
    """
    return date list from start_date, and end_date which are the input arguments
    """
    start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
    date_list = [ date.strftime("%Y-%m-%d") for date in date_generated]
    return date_list

def main(repo_owner, repo_name, start_date, end_date):
    """
    main function run ETL process : call github API get commit -> commit process -> commit to Postgre
    """
    print ('start_date : ', str(start_date), 'end_date : ', str(end_date))
    repo_url = 'https://api.github.com/repos/{}/{}/commits?since={}T00:00:00Z&until={}T23:59:59Z'.format(repo_owner, repo_name, start_date, end_date)
    df = Commit2df(repo_url)
    output_df = extract_inform(df)
    postgre_config = parse_config('config/postgre.config')
    dumptopostgre = DumpToPostgre()
    dumptopostgre.insert_all_to_table(output_df,'git_commit',postgre_config)
    time.sleep(3)  # sleep 3 sec after every scraping, avoid block by server

def run():
    if len(sys.argv) != 5:
        print (""" 
               Please run the etl.py script with valid arguments:
               python src/etl.py <repo_user> <repo_name> <start_date> <end_date>
               e.g. : python src/etl.py apache spark 2019-09-01 2019-10-30
               """)
        return 
    repo_owner, repo_name, start_date, end_date =  sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    date_list = daterange_2_datelist(start_date, end_date)
    [ main(repo_owner, repo_name, date, date) for date in date_list]

if __name__ == '__main__':
    run()
