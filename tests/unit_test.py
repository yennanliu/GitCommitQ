import datetime
import sys
sys.path.append(".")
from src.process_commit import (get_commit_timestamp as get_commit_timestamp_,
                                generate_id as generate_id_,
                                get_user_id as get_user_id_,
                                get_repo_url as get_repo_url_,
                                extract_inform as extract_inform_)
# from src.get_commit import * 
# from src.dump_to_postgre import * 
# from src.etl import * 

def test_generate_id():
    input_id = '4d17bc5e-bfbe-4cc9-b45b-2e879a190ce3'
    output = generate_id_(input_id) 
    assert len(output) == 36

def test_get_user_id():
    df_col = {'url': 'https://api.github.com/users/hanyucui', 'avatar_url': 'https://avatars0.githubusercontent.com/u/9649417?v=4', 'repos_url': 'https://api.github.com/users/hanyucui/repos', 'following_url': 'https://api.github.com/users/hanyucui/following{/other_user}', 'node_id': 'MDQ6VXNlcjk2NDk0MTc=', 'login': 'hanyucui', 'site_admin': False, 'html_url': 'https://github.com/hanyucui', 'starred_url': 'https://api.github.com/users/hanyucui/starred{/owner}{/repo}', 'events_url': 'https://api.github.com/users/hanyucui/events{/privacy}', 'gravatar_id': '', 'type': 'User', 'subscriptions_url': 'https://api.github.com/users/hanyucui/subscriptions', 'id': 9649417, 'organizations_url': 'https://api.github.com/users/hanyucui/orgs', 'received_events_url': 'https://api.github.com/users/hanyucui/received_events', 'gists_url': 'https://api.github.com/users/hanyucui/gists{/gist_id}', 'followers_url': 'https://api.github.com/users/hanyucui/followers'}
    output = get_user_id_(df_col)
    assert output == "https://github.com/hanyucui"

# def test_get_repo_url():
#     df_col = {'url': 'https://api.github.com/users/hanyucui', 'avatar_url': 'https://avatars0.githubusercontent.com/u/9649417?v=4', 'repos_url': 'https://api.github.com/users/hanyucui/repos', 'following_url': 'https://api.github.com/users/hanyucui/following{/other_user}', 'node_id': 'MDQ6VXNlcjk2NDk0MTc=', 'login': 'hanyucui', 'site_admin': False, 'html_url': 'https://github.com/hanyucui', 'starred_url': 'https://api.github.com/users/hanyucui/starred{/owner}{/repo}', 'events_url': 'https://api.github.com/users/hanyucui/events{/privacy}', 'gravatar_id': '', 'type': 'User', 'subscriptions_url': 'https://api.github.com/users/hanyucui/subscriptions', 'id': 9649417, 'organizations_url': 'https://api.github.com/users/hanyucui/orgs', 'received_events_url': 'https://api.github.com/users/hanyucui/received_events', 'gists_url': 'https://api.github.com/users/hanyucui/gists{/gist_id}', 'followers_url': 'https://api.github.com/users/hanyucui/followers'}
#     output = get_repo_url_(df_col)
#     assert output == "https://github.com/hanyucui"

def test_get_commit_timestamp():
    df_col = {'committer': {'date': '2019-01-01T05:17:13Z', 'name': 'Matei Zaharia', 'email': 'mateiz@users.noreply.github.com'}, 'url': 'https://api.github.com/repos/mlflow/mlflow/git/commits/b6550a79b5280dec95ae8e365ef647cc573eb3cd', 'message': 'Corrects the path to the multistep example (#787)', 'verification': {'verified': False, 'payload': None, 'reason': 'unsigned', 'signature': None}, 'tree': {'url': 'https://api.github.com/repos/mlflow/mlflow/git/trees/f830daeee06ad70db381a6a95309407d76a9c7c0', 'sha': 'f830daeee06ad70db381a6a95309407d76a9c7c0'}, 'comment_count': 0, 'author': {'date': '2019-01-01T05:17:13Z', 'name': 'Hanyu Cui', 'email': 'hanyu.cui@databricks.com'}}
    output = get_commit_timestamp_(df_col) 
    assert output == datetime.datetime(2019, 1, 1, 5, 17, 13)

# def test_extract_inform():
#     pass
    
if __name__ == '__main__':
    pytest.main([__file__])