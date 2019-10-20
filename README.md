<h1 align="center">GitCommitQ</h1>
<h3 align="center">ETL of Commits of a Github Repo</h3>

### Main scripts 
* [DB ddl](https://github.com/yennanliu/GitCommitQ/tree/master/ddl/versions)
* [config](https://github.com/yennanliu/GitCommitQ/blob/master/config/postgre.config)
* [ETL script](https://github.com/yennanliu/GitCommitQ/blob/master/src/etl.py)
* [analysis SQL](https://github.com/yennanliu/GitCommitQ/blob/master/sql/analysis.sql)

### Tech 
-  Python 3, PostgreSQL, Alembic, Docker

### File Structure
```
├── README.md
├── alembic.ini         : config for DDL alembic
├── config              : config for Postgre DB
├── data                : sample raw scraping data 
├── ddl                 : Postgre DDL via alembic 
├── requirements.txt    : Python dependency 
├── script              : Help script for etl, env set up 
├── sql                 : SQL get data as requirement   
└── src                 : Main scripts doing data process : etl.py 

```

### DB model

<details>
<summary>DB model</summary>

```
raw_commit(
    sa.Column('node_id',sa.String(length=256), primary_key=True),
    sa.Column('html_url', sa.String(length=256), nullable=True),
    sa.Column('comments_url',  sa.UnicodeText(), nullable=True),
    sa.Column('commit', sa.UnicodeText(), nullable=True),
    sa.Column('parents',  sa.String(length=512), nullable=True),
    sa.Column('sha', sa.String(length=256), nullable=True),
    sa.Column('author',  sa.UnicodeText(), nullable=True),
    sa.Column('url', sa.String(length=256), nullable=True),
    sa.Column('committer', sa.UnicodeText(), nullable=True),
    sa.PrimaryKeyConstraint('node_id') 
    )

commit_fact(
    sa.Column('user_id',sa.String(length=256)),
    sa.Column('commit_url', sa.String(length=256)),
    sa.Column('repo_url',  sa.String(length=256), nullable=True),
    sa.Column('commit_timestamp',  sa.TIMESTAMP(), nullable=True),
    sa.Column('commit_id', sa.String(length=256), primary_key=True),
    sa.PrimaryKeyConstraint('commit_id') 
    )

commit_contributor(
    sa.Column('user_id',sa.String(length=256)),
    sa.Column('last_commit_time',  sa.TIMESTAMP(), nullable=True),
    sa.Column('commit_count', sa.String(length=256), primary_key=True),
    sa.PrimaryKeyConstraint('user_id') 
    )

commited_repo(
    sa.Column('repo_url',  sa.String(length=256), nullable=True),
    sa.Column('committ_count', sa.String(length=256)),
    sa.Column('last_commited_timestamp',  sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('repo_url') 
    )

```

<details>


### Quick start

```bash
# STEP 0) : GET THE REPO 
$ cd ~ && git clone https://github.com/yennanliu/GitCommitQ.git
$ cd ~ && GitCommitQ
$ pip install -r requirements.txt

# STEP 1) INIT DB 
# run postgre local 
$ bash script/start_postgre.sh 
# make sure you replace postgre config with yours : config/postgre.config
# and create a postgre user : postgre_user with password : 0000
# and grant database access to user above 

# STEP 2) RUN DB MIGRATION 
$ alembic upgrade head

# STEP 3) RUN ETL DEMO 
$ python src/etl.py apache spark 2019-01-01 2019-10-18
$ python src/etl.py mlflow mlflow 2019-01-01 2019-10-18

# STEP 4) CHECK THE SCRAPING GIT DATA 

# Overview of the tables 
psql> \d 
              
                List of relations
 Schema |      Name       | Type  |    Owner     
--------+-----------------+-------+--------------
 public | alembic_version | table | postgre_user
 public | git_commit      | table | postgre_user
 public | raw_git_commit  | table | postgre_user
(3 rows)

# data overview 
psql> 
select * from git_commit limit 3;

          user_id           |                                             commit_url                                              |                 repo_url                  |  commit_timestamp   |              commit_id               
----------------------------+-----------------------------------------------------------------------------------------------------+-------------------------------------------+---------------------+--------------------------------------
 https://github.com/mdanatg | https://api.github.com/repos/tensorflow/tensorflow/commits/c7f3bb27278a2392b55cde6e3bd6714556511f9d | https://github.com/tensorflow/tensorflow/ | 2019-09-27 15:48:22 | b499cb40-6cf9-46d1-91f8-ee0ebb70a51f
 https://github.com/mrry    | https://api.github.com/repos/tensorflow/tensorflow/commits/250a5d47828aa229857266d59b32314bda79bcb3 | https://github.com/tensorflow/tensorflow/ | 2019-09-27 15:05:05 | 620240fd-7d40-4437-9df9-610a132aa84a
 https://github.com/alextp  | https://api.github.com/repos/tensorflow/tensorflow/commits/967e4a47f02c70e9978308f3410dd14821a1ac0b | https://github.com/tensorflow/tensorflow/ | 2019-09-27 14:28:27 | 4d17bc5e-bfbe-4cc9-b45b-2e879a190ce3
(3 rows)


# List the top 3 authors in the given time period 
psql> 

SELECT user_id
FROM
  (SELECT user_id,
          count(*)
   FROM git_commit
   WHERE commit_timestamp < '2019-10-01 00:08:00'
     AND commit_timestamp > '2019-01-01 00:08:00'
   GROUP BY 1
   ORDER BY 2 DESC
   LIMIT 3) sub; 


                 user_id                  
------------------------------------------
 https://github.com/smurching
 https://github.com/tensorflower-gardener
 https://github.com/dbczumar
(3 rows)


# Find the author with the longest contribution window within the time period?

psql>

SELECT distinct(user_id)
FROM git_commit
WHERE user_id IN
    (SELECT user_id
     FROM
       (SELECT user_id,
               max_commit_timestamp - min_commit_timestamp AS time_diff
        FROM
          (SELECT user_id,
                  max(commit_timestamp) AS max_commit_timestamp,
                  min(commit_timestamp) AS min_commit_timestamp
           FROM git_commit
           GROUP BY 1) sub
        ORDER BY time_diff DESC
        LIMIT 1) sub_); 

           user_id            
------------------------------
 https://github.com/smurching
(1 row)


# Produce a heatmap of commits 

psql>

WITH commit_weekday_hour AS
  (SELECT commit_id,
          date_part('minute', commit_timestamp)::float/60 + date_part('hour', commit_timestamp)::float AS HOUR,
          to_char(commit_timestamp, 'Day') AS weekday
   FROM git_commit),
     commit_weekday_hourgroup AS
  (SELECT *,
          CASE
              WHEN HOUR BETWEEN 0 AND 3 THEN '12am-3am'
              WHEN HOUR BETWEEN 3 AND 6 THEN '3am-6am'
              WHEN HOUR BETWEEN 6 AND 9 THEN '6am-9am'
              WHEN HOUR BETWEEN 9 AND 12 THEN '9am-12pm'
              WHEN HOUR BETWEEN 12 AND 15 THEN '12pm-3pm'
              WHEN HOUR BETWEEN 15 AND 18 THEN '3pm-6pm'
              WHEN HOUR BETWEEN 18 AND 21 THEN '6pm-9pm'
              WHEN HOUR BETWEEN 21 AND 24 THEN '9pm-12am'
              ELSE 'none'
          END AS hour_group
   FROM commit_weekday_hour)
SELECT hour_group,
       sum(CASE
               WHEN trim(weekday) = 'Sunday' THEN 1
               ELSE 0
           END) AS Sun,
       sum(CASE
               WHEN trim(weekday) = 'Monday' THEN 1
               ELSE 0
           END) AS Mon,
       sum(CASE
               WHEN trim(weekday) = 'Tuesday' THEN 1
               ELSE 0
           END) AS Tue,
       sum(CASE
               WHEN trim(weekday) = 'Wednesday' THEN 1
               ELSE 0
           END) AS Wed,
       sum(CASE
               WHEN trim(weekday) = 'Thursday' THEN 1
               ELSE 0
           END) AS Thur,
       sum(CASE
               WHEN trim(weekday) = 'Friday' THEN 1
               ELSE 0
           END) AS Fri,
       sum(CASE
               WHEN trim(weekday) = 'Saturday' THEN 1
               ELSE 0
           END) AS Sat
FROM commit_weekday_hourgroup
GROUP BY 1;

 hour_group | sun | mon | tue | wed | thur | fri | sat 
------------+-----+-----+-----+-----+------+-----+-----
 12am-3am   |   0 |   4 |   0 |   0 |   21 |  40 |  18
 12pm-3pm   |   0 |   0 |   0 |   0 |    6 |  35 |   0
 9pm-12am   |   4 |   0 |   0 |   0 |   55 |  30 |   0
 6am-9am    |   2 |   2 |   0 |   0 |    6 |  21 |   2
 3pm-6pm    |   0 |   0 |   0 |   0 |   36 |  37 |   2
 9am-12pm   |   4 |   2 |   0 |   0 |    6 |  28 |   4
 3am-6am    |   2 |   2 |   0 |   0 |    6 |  21 |   6
 6pm-9pm    |   4 |   0 |   0 |   0 |   42 |  40 |   2
(8 rows)

```