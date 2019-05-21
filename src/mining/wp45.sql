-- Create Players Match Efficiency View

.mode column 
.header ON

-- Calculate Players Efficiency per Match

.mode column 
.header ON

-- 1. Calculate the Number of Kills and the Number of Suicides per Player and Per Match


DROP TABLE IF EXISTS match_statistics
go
DROP VIEW IF EXISTS view_match_statistics
go

CREATE VIEW view_match_statistics AS
    select t1.match_id, t1.player_name, t1.kill_count,
    t2.death_count, t1.suicide_count, 
    ROUND(t1.kill_count * 100.0 / (t1.kill_count + t2.death_count + t1.suicide_count), 2) AS efficiency
    from
(
select a.*
from
(select players.match_id, players.player_name, count(case when match_frag.victim_name is not null then 1 end) as kill_count, count(case when match_frag.victim_name is null then 1 end) as suicide_count, 0 as death_count
from 
    (
        SELECT match_id, killer_name as player_name
        FROM match_frag
        UNION
        SELECT match_id, victim_name
        FROM match_frag
        WHERE victim_name is not null
    )
 as players 
left join match_frag on players.match_id = match_frag.match_id and players.player_name = match_frag.killer_name
group by players.match_id, players.player_name
UNION
-- SQL-02: Calculate the Number of Deaths per Player and Per Match
select players.match_id, players.player_name, 0, 0, count(*) as death_count
from 
    (
        SELECT match_id, killer_name as player_name
        FROM match_frag
        UNION
        SELECT match_id, victim_name
        FROM match_frag
        WHERE victim_name is not null
    )
 as players 
left join match_frag on players.match_id = match_frag.match_id and players.player_name = match_frag.victim_name
group by players.match_id, players.player_name) as a 
) as t1
--    though_statistic as t1 
    join 
(
select a.*
from
(select players.match_id, players.player_name, count(case when match_frag.victim_name is not null then 1 end) as kill_count, count(case when match_frag.victim_name is null then 1 end) as suicide_count, 0 as death_count
from 
    (
        SELECT match_id, killer_name as player_name
        FROM match_frag
        UNION
        SELECT match_id, victim_name
        FROM match_frag
        WHERE victim_name is not null
    )
as players 
left join match_frag on players.match_id = match_frag.match_id and players.player_name = match_frag.killer_name
group by players.match_id, players.player_name
UNION
-- SQL-02: Calculate the Number of Deaths per Player and Per Match
select players.match_id, players.player_name, 0, 0, count(*) as death_count
from 
    (
        SELECT match_id, killer_name as player_name
        FROM match_frag
        UNION
        SELECT match_id, victim_name
        FROM match_frag
        WHERE victim_name is not null
    )
as players 
left join match_frag on players.match_id = match_frag.match_id and players.player_name = match_frag.victim_name
group by players.match_id, players.player_name) as a 
) as t2  
--    though_statistic as t2
    on t1.match_id = t2.match_id and t1.player_name = t2.player_name
    and not(t1.kill_count = t2.kill_count and t1.suicide_count = t2.suicide_count or t1.death_count = t2.death_count)
    where t1.kill_count + t2.death_count + t1.suicide_count <> 0
go 

select * from view_match_statistics
order by efficiency ASC