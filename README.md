<h1 align="center">GitCommitQ</h1>
ETL of Commits of a Github Repo

### Main scripts 
[DB ddl](https://github.com/yennanliu/GitCommitQ/tree/master/ddl/versions)
[DB config](https://github.com/yennanliu/GitCommitQ/blob/master/config/postgre.config)
[ETL script](https://github.com/yennanliu/GitCommitQ/blob/master/src/etl.py)
[analysis SQL](https://github.com/yennanliu/GitCommitQ/blob/master/sql/analysis.sql)

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

### Quick start

```bash
# STEP 0) : GET THE REPO 
$ cd ~ && git clone https://github.com/yennanliu/GitCommitQ.git
$ cd ~ && GitCommitQ
$ git install -r requirements.txt

# STEP 1) INIT DB 
# run postgre local 
$ bash script/start_postgre.sh 
# make sure you replace postgre config with yours : config/postgre.config
# and create a postgre user : postgre_user with password : 0000
# and grant database access to user above 

# STEP 2) RUN DB MIGRATION 
$ alembic upgrade head

# STEP 3) RUN ETL DEMO 
$ python src/etl.py tensorflow tensorflow git_commit
$ python src/etl.py mlflow  mlflow git_commit

# STEP 4) CHECK THE SCRAPING GIT DATA 

# Overview of the tables 
psql> /d 
              
                List of relations
 Schema |      Name       | Type  |    Owner     
--------+-----------------+-------+--------------
 public | alembic_version | table | postgre_user
 public | git_commit      | table | postgre_user
 public | raw_git_commit  | table | postgre_user
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
          date_part('hour', commit_timestamp) AS HOUR,
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
           END) AS Fri
FROM commit_weekday_hourgroup
GROUP BY 1;

 hour_group | sun | mon | tue | wed | thur | fri 
------------+-----+-----+-----+-----+------+-----
 6pm-9pm    |   1 |  28 |   6 |   2 |    1 |   5
 6am-9am    |   2 |   3 |   8 |   1 |    0 |   0
 3am-6am    |   3 |   4 |  10 |   0 |    2 |   0
 12am-3am   |   1 |   4 |  18 |   4 |    4 |   1
 9am-12pm   |   0 |   1 |   1 |   0 |    0 |   0
 12pm-3pm   |   0 |   3 |   0 |   0 |    0 |   1
 3pm-6pm    |   2 |  31 |   5 |   4 |    3 |   6
 9pm-12am   |   2 |  12 |   7 |   2 |    1 |   3
(8 rows)

```