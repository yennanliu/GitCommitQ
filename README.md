# GitCommitQ
ETL of Commits of a Github Repo

### Quick start

```bash
$ cd ~ && git clone https://github.com/yennanliu/GitCommitQ.git
$ cd ~ && GitCommitQ
$ git install -r requirements.txt
# run postgre local 
$ bash script/start_postgre.sh 
$ python src/etl.py tensorflow tensorflow git_commit
```