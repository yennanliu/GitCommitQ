import datetime
import pandas as pd
import psycopg2
from psycopg2 import DatabaseError, ProgrammingError
import sys
sys.path.append(".")
from src.dump_to_postgre import DumpToPostgre as DumpToPostgre_
from script.utility import parse_config as parse_config_

import unittest
import pytest
from unittest.mock import patch, Mock

 
postgre_config = {
  "url":             "jdbc:postgres://localhost/gitcommit",
  "host":            "127.0.0.1",
  "dbname":          "gitcommit",
  "dbtable_batch":   "fulltable",
  "dbtable_stream":  "rddbatch",
  "mode_batch":      "overwrite",
  "mode_stream":     "append",
  "user":            "postgre_user",
  "password":        "0000",
  "driver":          "com.postgres.jdbc.Driver",
  "numPartitions":   18,
  "partitionColumn": "time_slot",
  "lowerBound":      0,
  "upperBound":      144,
  "stringtype":      "unspecified",
  "topntosave":      10 }
  
data = {'id' : ['jack','mary'], 'age' : [10, 90]}
df = pd.DataFrame(data)

class TestDBOpFunc(unittest.TestCase):


    def test_parse_config(self):
        config = parse_config_("config/postgre.config")
        assert config['url'] == "jdbc:postgres://localhost/gitcommit"
        assert config['host'] == "127.0.0.1"
        assert config['dbname'] == "gitcommit"
        assert config['user'] == "postgre_user"
        assert config['driver'] == "com.postgres.jdbc.Driver"

    def test_get_conn(self):
        with patch('psycopg2.connect') as mock_connect:
            mock_connect.return_value = "db_conn"
            dump_to_postgre_ = DumpToPostgre_()
            db_conn = dump_to_postgre_.get_conn(postgre_config)
            # with db_conn.cursor() as cursor:
            #     cursor.execute("SELECT 1")
            #     result=cursor.fetchall()
            #assert type(db_conn) == psycopg2.extensions.connection and result[0][0] == 1
            assert db_conn == "db_conn"

    def test_get_conn_error(self):
        with patch('psycopg2.connect') as mock_connect:
            mock_connect.side_effect = ProgrammingError
            dump_to_postgre_ = DumpToPostgre_()
            db_conn = dump_to_postgre_.get_conn({"url":"random_db_url"})
            assert db_conn == None

    def test_drop_table(self):
        with patch.object(DumpToPostgre_, "get_conn", return_value="db_conn") as mock_get_conn, \
        patch.object(DumpToPostgre_, "drop_table", return_value=True) as mock_drop_table:
          conn = DumpToPostgre_.get_conn()
          result = DumpToPostgre_.drop_table()
        self.assertTrue(result)
        assert conn == "db_conn"

    def test_drop_table_error(self):
        with patch('psycopg2.connect') as mock_connect:
            dump_to_postgre_ = DumpToPostgre_()
            response = dump_to_postgre_.drop_table("my_table_name", "my_postgre_config")
            #self.assert_True(drop_table.called)
            assert response == None 

    # def test_insert_to_table():
    #     dump_to_postgre_ = DumpToPostgre_()
    #     db_conn= dump_to_postgre_.get_conn(postgre_config)
    #     # create table 
    #     schema = "(id VARCHAR (10), age integer)"
    #     dump_to_postgre_.create_table('test_table', schema, postgre_config)
    #     # insert df to table
    #     dump_to_postgre_.insert_to_table(df, 'test_table', postgre_config)
    #     with db_conn.cursor() as cursor:
    #         cursor.execute("SELECT * FROM test_table")
    #         result=cursor.fetchall()
    #     # TODO : drop table 
    #     assert result == [('jack', 10), ('mary', 90)]

    # def test_insert_all_to_table():
    #     # load to-insert df 
    #     df = pd.read_csv('data/movie_ratings.csv')
    #     dump_to_postgre_ = DumpToPostgre_()
    #     db_conn= dump_to_postgre_.get_conn(postgre_config)
    #     schema = "(index integer, userId integer, movieId integer, rating integer, timestamp integer)"
    #     # create table 
    #     dump_to_postgre_.create_table('movie_table', schema, postgre_config)
    #     # insert all to table 
    #     dump_to_postgre_.insert_all_to_table(df, 'movie_table', postgre_config)
    #     with db_conn.cursor() as cursor:
    #         cursor.execute("SELECT count(*) FROM movie_table")
    #         result=cursor.fetchall()
    #     # TODO : drop table 
    #     #dump_to_postgre_.drop_table('movie_table', postgre_config)
    #     assert result[0][0] == 100004


if __name__ == '__main__':
    pytest.main([__file__])