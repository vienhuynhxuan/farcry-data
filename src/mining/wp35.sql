-- Calculate the Number of Kills (1)

.mode column 
.header ON

SELECT COUNT(*) as kill_count
FROM match_frag
WHERE victim_name is not NULL
