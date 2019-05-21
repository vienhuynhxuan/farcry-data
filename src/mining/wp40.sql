-- Calculate and Order the Total Number of Kills per Player

.mode column 
.header on

SELECT killer_name as player_name, COUNT(*) as kill_count
FROM match_fRag
WHERE victim_name is not NULL
GROUP BY killer_name
ORDER BY kill_count DESC, killer_name ASC