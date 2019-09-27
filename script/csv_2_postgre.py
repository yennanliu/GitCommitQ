import sys
sys.path.append("./script/")
import pandas as pd 
import psycopg2
import uuid 
# UDF 
from utility import * 

def fix_csv_form(df, csv_name):
    """
    fix csv form, make it dump to mysql OK 
    """
    if 'Unnamed: 0' in df.columns: del df['Unnamed: 0']  # remove 'Unnamed: 0' at df here, will fix this workaround later
    return df 

def generate_id(x):
    """
    generate tip id from user id, since tip id not exists in orgin data  
    """
    return str(uuid.uuid4())

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
    cols = "`,`".join([str(i) for i in df.columns.tolist()])
    for i,row in df.iterrows():
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO {} (" + cols.strip("'") + ") VALUES (" + "%s,"*(len(row)-1) + "%s)"
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

def main(csv_name, table_name):
    """
    python function load csv, fix csv form, and dump fixed csv data into mysql  
    : input  : pandas dataframe 
    : output : mysql data 
    """
    print ('>>>>> process : {} --> {}'.format(csv_name, table_name))
    postgre_config = parse_config('config/postgre.config')
    conn = get_conn(postgre_config)
    df = pd.read_csv(csv_name, index_col=False)
    df = fix_csv_form(df, csv_name)
    insert_to_table(df,table_name, conn)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])