-- Calculate and Order the Number of Kills per Player and per Match

.mode column 
.header ON

SELECT match_id, killer_name as player_name, COUNT(*) as kill_count
FROM match_frag
WHERE victim_name is not NULL
GROUP BY match_id, killer_name
ORDER BY match_id, kill_count DESC