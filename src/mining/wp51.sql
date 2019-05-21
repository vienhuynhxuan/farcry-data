-- Determine Players Worst Enemy

select match_id, killer_name as player_name, victim_name as worst_enemy_name, kill_count
from
    (select
        row_number() over (
            PARTITION BY match_id, victim_name
            order by kill_count desc
        ) rank, match_id, killer_name, victim_name as victim_name, kill_count
    from 
        (select match_id, killer_name, victim_name, count(*) as kill_count
        from match_frag
        where victim_name is not null
        group by match_id, killer_name, victim_name) as counting) as ranking
where ranking.rank = 1
order by match_id, killer_name;
