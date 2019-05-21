-- Calculate and Order the Number of Suicides per Match

.mode column 
.header ON

SELECT match_id, count(*) as suicide_count
FROM match_frag
WHERE victime_name is NULL
GROUP BY match_id
ORDER BY suicide_count