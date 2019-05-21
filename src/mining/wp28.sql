-- Select Game Mode and Map Name of Matches

.mode column
.header on 

SELECT match_id, game_mode, map_name
FROM match
