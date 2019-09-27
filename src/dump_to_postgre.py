import sys
sys.path.append("./script/")
import psycopg2
# UDF 
from utility import * 

def get_conn(postgre_config):
    """
    Connect to the database
    """
    # connection = psycopg2.connect(host=postgre_config['host'],
    #  user=postgre_config['user'],
    #  password=postgre_config['password'],
    #  db=postgre_config['dbname'],
    #  charset='utf8mb4',
    #  cursorclass=psycopg2.cursors.DictCursor)
    connection = psycopg2.connect(
        database=postgre_config['dbname'], 
        user=postgre_config['user'],
        password=postgre_config['password'],)
    return connection

def insert_to_table(df,table_name,connection):
    """
    auto visit columns in dataframe, parse row data, and insert to postgre 
    """
    cols = ",".join([str(i) for i in df.columns.tolist()])
    for i,row in df.iterrows():
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO {} (" + cols + ") VALUES (" + "%s,"*(len(row)-1) + "%s)"
                #sql = "INSERT INTO {} (" +cols + ") VALUES (" + "%s,"*(len(row)-1) + "%s)"
                #cur.execute("INSERT INTO cars(name, price) VALUES('Audi', 52642)")
                sql = sql.format(table_name)
                print (sql)
                cursor.execute(sql, tuple(row))
                connection.commit()
                print ('insert ok')
        except Exception as e:
            print (e, 'insert failed', i, row)
    connection.close()
    cursor.close()
