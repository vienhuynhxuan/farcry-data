-- Calculate and Order the Number of Kills and Suicides per Match

.mode column 
.header ON

SELECT match_id, count(*) as kill_suicide_count
FROM match_frag
GROUP BY match_id
ORDER BY kill_suicide_count DESC