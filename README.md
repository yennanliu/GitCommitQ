# GitCommitQ
ETL of Commits of a Github Repo

### Tech 
-  Python 3, PostgreSQL, Alembic, Docker

### Quick start

```bash
$ cd ~ && git clone https://github.com/yennanliu/GitCommitQ.git
$ cd ~ && GitCommitQ
$ git install -r requirements.txt
# run postgre local 
$ bash script/start_postgre.sh 
# make sure you replace postgre config with yours : config/postgre.config
# and create a postgre user : postgre with password : 0000
# and grant database access to user above 
$ python src/etl.py tensorflow tensorflow git_commit
```