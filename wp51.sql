-- Determine Players Worst Enemy


CREATE TEMP TABLE temp_players_favorite_victims AS
select match_id, killer_name, victim_name as worst_enemy_name, kill_count
from
    (select
        row_number() over (
            PARTITION BY match_id, killer_name
            order by kill_count desc
        ) rank, match_id, killer_name, victim_name as victim_name, kill_count
    from 
        (select match_id, killer_name, victim_name, count(*) as kill_count
        from match_frag
        where victim_name is not null
        group by match_id, killer_name, victim_name) as counting) as ranking
where ranking.rank = 1
order by match_id, killer_name;

select * from temp_players_favorite_victims 

/*not remove duplicate yet (duplicate: temp_players_favorite_victims)*/
