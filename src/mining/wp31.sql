-- Order the List of Killer Names

.mode column 
.header ON

SELECT DISTINCT killer_name
FROM match_flag
ORDER BY killer_name