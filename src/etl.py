import sys
sys.path.append("./script/")
# UDF 
from utility import * 
from get_commit import *
from process_commit import *
from dump_to_postgre import * 

def main(repo_url, table_name):
	df = Commit2df(repo_url)
	output_df = extract_inform(df)
	postgre_config = parse_config('config/postgre.config')
	connection = get_conn(postgre_config)
	insert_to_table(output_df,table_name,connection)

if __name__ == '__main__':
    repo_url = 'https://api.github.com/repos/apache/airflow/commits'
    table_name = 'git_commit'
    main(repo_url, table_name)