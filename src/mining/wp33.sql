-- Calculate the number of Kills and Suicides

.mode column 
.header ON

SELECT COUNT(killer_name) as kill_suicide_count
FROM match_frag