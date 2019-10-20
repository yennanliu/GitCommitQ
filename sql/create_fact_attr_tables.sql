-- sql clean commit, and create commit fact table 

DROP TABLE IF EXISTS commit_fact;
CREATE TABLE commit_fact AS WITH cleaned_commit AS
  (SELECT DISTINCT user_id as commitor_id,
                   commit_timestamp,
                   commit_url,
                   repo_url as repo_id
   FROM git_commit
   where repo_url is not Null)
SELECT *
FROM cleaned_commit;

-- sql build commitor table (repo code contributor)

DROP TABLE IF EXISTS commit_commitor;
CREATE TABLE commit_commitor AS WITH commitor AS
  (SELECT commitor_id,
          min(commit_timestamp) AS first_commit_time,
          max(commit_timestamp) AS last_commit_time,
          count(*) AS commit_count
   FROM commit_fact
   GROUP BY 1)
SELECT *
FROM commitor;


-- sql build commited repo (repo contributed by the commitor) 

DROP TABLE IF EXISTS commited_repo;
CREATE TABLE commited_repo AS WITH repo AS
  (SELECT repo_id,
          min(commit_timestamp) AS first_commited_time,
          max(commit_timestamp) AS last_commited_time,
          count(*) AS commited_count
   FROM commit_fact
   GROUP BY 1)
SELECT *
FROM repo;







