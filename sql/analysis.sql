-- List the top 3 authors in the given time period

SELECT user_id
FROM
  (SELECT user_id,
          count(*)
   FROM git_commit
   WHERE commit_timestamp < '2019-10-01 00:08:00'
     AND commit_timestamp > '2019-01-01 00:08:00'
   GROUP BY 1
   ORDER BY 2 DESC
   LIMIT 3) sub

-- Find the author with the longest contribution window within the time period?

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
        LIMIT 1) sub_)

-- Produce a heatmap of commits 
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
