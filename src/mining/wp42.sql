-- Calculate and Order the Number of Deaths per Player and per Match

.mode column 
.header ON

SELECT match_id, victim_name as player_name, COUNT(*) as death_count
FROM match_frag
WHERE victim_name is not NULL
GROUP BY match_id, victim_name
ORDER BY match_id, death_count DESC


