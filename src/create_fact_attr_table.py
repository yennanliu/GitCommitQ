import sys
sys.path.append("./script/")
import datetime
import time
# UDF 
from utility import parse_config 
from dump_to_postgre import DumpToPostgre 

sql_commit_fact = """ 
DROP TABLE IF EXISTS commit_fact;
CREATE TABLE commit_fact AS WITH cleaned_commit AS
  (SELECT DISTINCT user_id as commitor_id,
                   commit_timestamp,
                   commit_url,
                   repo_url as repo_id
   FROM git_commit
   where repo_url is not Null)
SELECT *
FROM cleaned_commit;
"""

sql_commit_commitor = """

DROP TABLE IF EXISTS commit_commitor;
CREATE TABLE commit_commitor AS WITH commitor AS
  (SELECT commitor_id,
          min(commit_timestamp) AS first_commit_time,
          max(commit_timestamp) AS last_commit_time,
          count(*) AS commit_count
   FROM commit_fact
   GROUP BY 1)
SELECT *
FROM commitor;
"""

sql_commited_repo = """
DROP TABLE IF EXISTS commited_repo;
CREATE TABLE commited_repo AS WITH repo AS
  (SELECT repo_id,
          min(commit_timestamp) AS first_commited_time,
          max(commit_timestamp) AS last_commited_time,
          count(*) AS commited_count
   FROM commit_fact
   GROUP BY 1)
SELECT *
FROM repo;
"""

def main():
    postgre_config = parse_config('config/postgre.config')
    dumptopostgre = DumpToPostgre()
    connection = dumptopostgre.get_conn(postgre_config)
    sql_list = [sql_commit_fact, sql_commit_commitor, sql_commited_repo] 
    for sql in sql_list: 
        try:
            with connection.cursor() as cursor:
                print (sql)
                cursor.execute(sql)
                connection.commit()
                print ('>>>> table build ok')
        except Exception as e:
            print ('>>>> table build failed', str(e))

if __name__ == '__main__':
    main()