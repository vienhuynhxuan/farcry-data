-- Calculate the Number of Suicides

.mode column 
.header ON

SELECT COUNT(*) as suicide_count
FROM match_frag
WHERE victim_name is NULL