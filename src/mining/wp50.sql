-- Determine Players Favorite Victim

CREATE TEMP TABLE temp_players_favorite_victims AS
select match_id, killer_name, favorite_victim_name, kill_count
from
    (select
        row_number() over (
            PARTITION BY match_id, victim_name
            order by kill_count desc
        ) rank, match_id, killer_name, victim_name as favorite_victim_name, kill_count
    from 
        (select match_id, killer_name, victim_name, count(*) as kill_count
        from match_frag
        where victim_name is not null
        group by match_id, killer_name, victim_name) as counting) as ranking
where ranking.rank = 1
order by match_id, favorite_victim_name;


select * from temp_players_favorite_victims 
order by match_id, killer_name, favorite_victim_name
/*not remove duplicate yet (duplicate: temp_players_favorite_victims)*/

