import sys
sys.path.append("./script/")
import psycopg2
# UDF 
from utility import * 

class DumpToPostgre:

    def get_conn(self, postgre_config):
        """
        Connect to the database
        """
        connection = psycopg2.connect(
            database=postgre_config['dbname'], 
            user=postgre_config['user'],
            password=postgre_config['password'],)
        return connection

    def insert_to_table(self, df, table_name, postgre_config):
        """
        auto visit columns in dataframe, parse row data, and insert to postgre 
        """
        connection = self.get_conn(postgre_config)
        cols = ",".join([str(i) for i in df.columns.tolist()])
        for i,row in df.iterrows():
            try:
                with connection.cursor() as cursor:
                    sql = "INSERT INTO {} (" + cols + ") VALUES (" + "%s,"*(len(row)-1) + "%s)"
                    sql = sql.format(table_name)
                    print (sql)
                    cursor.execute(sql, tuple(row))
                    connection.commit()
                    print ('insert ok')
            except Exception as e:
                print (e, 'insert failed', i, row)
        connection.close()
        cursor.close()

    def insert_all_to_table(self, df, table_name, postgre_config):
        """
        insert whole df to postgre once by executemany method
        """
        if len(df) == 0:
            print ('Null data, pass data insert')
            return 
        connection = self.get_conn(postgre_config)
        cols = ",".join([str(i) for i in df.columns.tolist()])
        to_insert = df.values.tolist()
        try:
            with connection.cursor() as cursor:
                #sql = "INSERT INTO git_commit (user_id,commit_url,repo_url,commit_timestamp,commit_id) VALUES (%s,%s,%s,%s,%s)"
                sql = "INSERT INTO {} (" + cols + ") VALUES (%s,%s,%s,%s,%s)"
                sql = sql.format(table_name)
                print (sql)
                cursor.executemany(sql, to_insert)
                connection.commit()
                print ('all insert ok')
        except Exception as e:
            print (e, 'all insert failed')
        connection.close()
        cursor.close()
