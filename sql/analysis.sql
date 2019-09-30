-- List the top 3 authors in the given time period?
SELECT user_id
FROM
  (SELECT user_id,
          count(*)
   FROM git_commit
   WHERE commit_timestamp < <given_timestamp1>
     AND commit_timestamp > <given_timestamp2>
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