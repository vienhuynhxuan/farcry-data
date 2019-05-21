-- Select Matches and Calculate the Number of Players and the Number of Kills and Suicides

.mode column 
.header ON

SELECT A.match_id, A.start_time, A.end_time, B.player_count, A.kill_suicide_count
FROM
    (SELECT match.match_id, start_time, end_time, COUNT(*) as kill_suicide_count
    FROM match LEFT JOIN match_frag ON match.match_id = match_frag.match_id
    GROUP BY match.match_id) as A
    JOIN    
   (SELECT temp.match_id, COUNT(*) as player_count
    FROM
        (SELECT match_id, killer_name as player_name
        FROM match_frag
        UNION
        SELECT match_id, victim_name
        FROM match_frag
        WHERE victim_name is not null) as temp
    GROUP BY temp.match_id) AS B
    ON A.match_id = B.match_id
