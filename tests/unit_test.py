import sys
sys.path.append(".")
from src.process_commit import * 
# from src.get_commit import * 
# from src.dump_to_postgre import * 
# from src.etl import * 


def test_get_commit_timestamp():
    df_col = {'committer': {'date': '2019-01-01T05:17:13Z', 'name': 'Matei Zaharia', 'email': 'mateiz@users.noreply.github.com'}, 'url': 'https://api.github.com/repos/mlflow/mlflow/git/commits/b6550a79b5280dec95ae8e365ef647cc573eb3cd', 'message': 'Corrects the path to the multistep example (#787)', 'verification': {'verified': False, 'payload': None, 'reason': 'unsigned', 'signature': None}, 'tree': {'url': 'https://api.github.com/repos/mlflow/mlflow/git/trees/f830daeee06ad70db381a6a95309407d76a9c7c0', 'sha': 'f830daeee06ad70db381a6a95309407d76a9c7c0'}, 'comment_count': 0, 'author': {'date': '2019-01-01T05:17:13Z', 'name': 'Hanyu Cui', 'email': 'hanyu.cui@databricks.com'}}
    output = get_commit_timestamp(df_col) 
    expected_output = datetime.datetime(2019, 1, 1, 5, 17, 13)
    assert output == expected_output

if __name__ == '__main__':
    pytest.main([__file__])