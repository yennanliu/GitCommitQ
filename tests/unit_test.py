import datetime
import sys
sys.path.append(".")
from src.process_commit import (get_commit_timestamp as get_commit_timestamp_,
                                generate_id as generate_id_)
# from src.get_commit import * 
# from src.dump_to_postgre import * 
# from src.etl import * 

def test_generate_id_():
    input_id = '4d17bc5e-bfbe-4cc9-b45b-2e879a190ce3'
    output = generate_id_(input_id) 
    assert len(output) == 36

def test_get_commit_timestamp():
    df_col = {'committer': {'date': '2019-01-01T05:17:13Z', 'name': 'Matei Zaharia', 'email': 'mateiz@users.noreply.github.com'}, 'url': 'https://api.github.com/repos/mlflow/mlflow/git/commits/b6550a79b5280dec95ae8e365ef647cc573eb3cd', 'message': 'Corrects the path to the multistep example (#787)', 'verification': {'verified': False, 'payload': None, 'reason': 'unsigned', 'signature': None}, 'tree': {'url': 'https://api.github.com/repos/mlflow/mlflow/git/trees/f830daeee06ad70db381a6a95309407d76a9c7c0', 'sha': 'f830daeee06ad70db381a6a95309407d76a9c7c0'}, 'comment_count': 0, 'author': {'date': '2019-01-01T05:17:13Z', 'name': 'Hanyu Cui', 'email': 'hanyu.cui@databricks.com'}}
    output = get_commit_timestamp_(df_col) 
    expected_output = datetime.datetime(2019, 1, 1, 5, 17, 13)
    assert output == expected_output

if __name__ == '__main__':
    pytest.main([__file__])