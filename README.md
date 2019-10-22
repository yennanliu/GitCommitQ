<h1 align="center">GitCommitQ</h1>
<h3 align="center">ETL of Commits of a Github Repo</h3>

### Main scripts 
* [DB ddl](https://github.com/yennanliu/GitCommitQ/tree/master/ddl/versions) - DB description language (DDL) build DB via migration
* [config](https://github.com/yennanliu/GitCommitQ/blob/master/config) - config files for DB connections
* [ETL : etl.py](https://github.com/yennanliu/GitCommitQ/blob/master/src/etl.py) - etl call Github API, process/transform/clean the data, and insert to Postgre
* [ETL : create_fact_attr_table.py](https://github.com/yennanliu/GitCommitQ/blob/master/src/create_fact_attr_table.py) - etl generate facts/attribution tables in Postgre 
* [SQL](https://github.com/yennanliu/GitCommitQ/blob/master/sql) - SQL build tables and get needed insights

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

### Workflow
```
Github      ----- etl.py ------>  PostgreSQL
               (scrape data)      ↓        ↑
                                  ↓        ↑
                                  ↓________↑
                              create_fact_attr_tables.py 
                               (sync Postgre tables)
```


### DB model

<details>
<summary>DB model</summary>

```
git_commit(
    sa.Column('user_id',sa.String(length=256)),
    sa.Column('commit_url', sa.String(length=256)),
    sa.Column('repo_url',  sa.String(length=256), nullable=True),
    sa.Column('commit_timestamp',  sa.TIMESTAMP(), nullable=True),
    sa.Column('commit_id', sa.String(length=256), primary_key=True),
    sa.PrimaryKeyConstraint('commit_id') 
    )

commit_fact(
    sa.Column('user_id',sa.String(length=256)),
    sa.Column('commit_timestamp',  sa.TIMESTAMP()),    
    sa.Column('commit_url', sa.String(length=256),  primary_key=True),
    sa.PrimaryKeyConstraint('commit_url') 
    )

commit_commitor(
    sa.Column('commitor_id',sa.String(length=256), primary_key=True),
    sa.Column('first_commit_time',  sa.TIMESTAMP(), nullable=True),
    sa.Column('last_commit_time',  sa.TIMESTAMP(), nullable=True),    
    sa.Column('commit_count', sa.integer()),
    sa.PrimaryKeyConstraint('commitor_id') 
    )

commited_repo(
    sa.Column('repo_id',  sa.String(length=256),  primary_key=True),
    sa.Column('first_commited_time',  sa.TIMESTAMP(), 
    sa.Column('last_commited_timestamp',  sa.TIMESTAMP(),     
    sa.Column('commited_count', sa.integer()),
    sa.PrimaryKeyConstraint('repo_id') 
    )
```

</details>


### Quick start


<details>
<summary>Quick start</summary>

```bash
############ PART A) : PROCESS/INSERT DATA

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

# STEP 3) RUN ETL 1 - data collect
$ python src/etl.py apache spark 2019-01-01 2019-01-31
$ python src/etl.py mlflow mlflow 2019-01-01 2019-01-31

# STEP 3) RUN ETL 2 -  create fact/attribution tables 
$ python src/create_fact_attr_table.py

```

```bash
############ PART B) : ANALYSIS WITH DATA

# STEP 4) CHECK THE SCRAPING GIT DATA 

# Overview of the tables 
psql> \d 
              
                List of relations
 Schema |      Name       | Type  |    Owner     
--------+-----------------+-------+--------------
 public | alembic_version | table | postgre_user
 public | commit_commitor | table | postgre_user
 public | commit_fact     | table | postgre_user
 public | commited_repo   | table | postgre_user
 public | git_commit      | table | postgre_user
 public | raw_git_commit  | table | postgre_user
(6 rows)

# data overview 
psql> 
select * from git_commit limit 3;

          user_id           |                                             commit_url                                              |                 repo_url                  |  commit_timestamp   |              commit_id               
----------------------------+-----------------------------------------------------------------------------------------------------+-------------------------------------------+---------------------+--------------------------------------
 https://github.com/mdanatg | https://api.github.com/repos/tensorflow/tensorflow/commits/c7f3bb27278a2392b55cde6e3bd6714556511f9d | https://github.com/tensorflow/tensorflow/ | 2019-09-27 15:48:22 | b499cb40-6cf9-46d1-91f8-ee0ebb70a51f
 https://github.com/mrry    | https://api.github.com/repos/tensorflow/tensorflow/commits/250a5d47828aa229857266d59b32314bda79bcb3 | https://github.com/tensorflow/tensorflow/ | 2019-09-27 15:05:05 | 620240fd-7d40-4437-9df9-610a132aa84a
 https://github.com/alextp  | https://api.github.com/repos/tensorflow/tensorflow/commits/967e4a47f02c70e9978308f3410dd14821a1ac0b | https://github.com/tensorflow/tensorflow/ | 2019-09-27 14:28:27 | 4d17bc5e-bfbe-4cc9-b45b-2e879a190ce3
(3 rows)

psql>
select * from commit_fact limit 3;
               commitor_id                |  commit_timestamp   |                                             commit_url                                              |                  repo_id                  
------------------------------------------+---------------------+-----------------------------------------------------------------------------------------------------+-------------------------------------------
 https://github.com/tomhennigan           | 2019-09-30 08:34:24 | https://api.github.com/repos/tensorflow/tensorflow/commits/a5afbfbd7a03596d74e99e6f65c1809a0561732b | https://github.com/tensorflow/tensorflow/
 https://github.com/tensorflower-gardener | 2019-09-30 09:02:51 | https://api.github.com/repos/tensorflow/tensorflow/commits/c4756e3a9939ada157055c881c6cf6e5d4f9c2dc | https://github.com/tensorflow/tensorflow/
 https://github.com/anj-s                 | 2019-09-27 21:00:43 | https://api.github.com/repos/tensorflow/tensorflow/commits/35d3ccf6a6893c82ad6b1c49cbebd47625e902b3 | https://github.com/tensorflow/tensorflow/
(3 rows)

psql>
select * from commit_commitor limit 3;

         commitor_id          |  first_commit_time  |  last_commit_time   | commit_count 
------------------------------+---------------------+---------------------+--------------
 https://github.com/deven-amd | 2019-09-27 06:49:51 | 2019-09-27 06:49:51 |            1
 https://github.com/gmagogsfm | 2019-09-27 23:20:04 | 2019-09-30 00:27:03 |            3
 https://github.com/fdxmw     | 2019-09-26 19:29:22 | 2019-09-27 19:42:51 |            3
(3 rows)

psql>
select * from commited_repo limit 3;

                  repo_id                  | first_commited_time | last_commited_time  | commited_count 
-------------------------------------------+---------------------+---------------------+----------------
 https://github.com/tensorflow/tensorflow/ | 2019-09-26 00:23:29 | 2019-09-30 09:02:51 |            176
(1 row)

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
 12am-3am   |  12 |  21 |  37 | 116 |   81 |  69 |  32
 12pm-3pm   |   6 |  18 |  84 |  47 |   26 |  42 |  27
 9pm-12am   |  23 |  53 | 149 |  46 |   69 |  65 |  10
 6am-9am    |   9 |  11 |  29 |  20 |   27 |  34 |   9
 3pm-6pm    |   9 |  33 | 181 |  70 |   61 |  59 |  15
 9am-12pm   |   5 |  12 |  16 |   9 |   21 |  30 |   6
 3am-6am    |  16 |  19 |  33 |  72 |   20 |  45 |  15
 6pm-9pm    |  16 |  35 | 172 |  70 |   60 |  74 |  14
(8 rows)

```
</details>