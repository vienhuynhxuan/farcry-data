-- Determine the Most Versatile Killer
select match_id, killer_name, count(distinct weapon_code) as weapon_count
from match_frag
group by match_id, killer_name
order by match_id, weapon_count