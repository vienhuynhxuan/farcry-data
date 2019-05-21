CREATE FUNCTION get_killer_class(weapon text) RETURNS text AS $$
BEGIN
    IF weapon IN ('Machete', 'Falcon', 'MP5')
        THEN RETURN 'Hitman';
    ELSIF weapon = 'SniperRifle'
        THEN RETURN 'Sniper';
    ELSIF weapon IN ('AG36', 'OICW', 'P90', 'M4', 'Shotgun', 'M249')
        THEN RETURN 'Commando';    
    ELSIF weapon IN (
                    'Rocket', 'VehicleRocket', 'HandGrenade', 'StickExplosive',
                    'Boat', 'Vehicle', 
                    'VehicleMountedRocketMG', 'VehicleMountedAutoMG', 'MG',
                    'VehicleMountedMG', 'OICWGrenade', 
                    'AG36GrenadeBoat', 'Vehicle', 'VehicleMountedRocketMG',
                    'VehicleMountedAutoMG',
                    'MG', 'VehicleMountedMG', 'OICWGrenade', 'AG36Grenade')
        THEN RETURN 'Psychopath';
    ELSE RETURN '????';
    END IF;
END; $$
LANGUAGE PLPGSQL;


-- select match_id, killer_name, weapon_code, count(*) as kill_count, get_killer_class(weapon_code) AS killer_class
-- from match_frag
-- where weapon_code is not null
-- group by match_id, killer_name, weapon_code;

-- select *
-- from match_frag
-- where weapon_code NOT IN 
-- ('Machete', 'Falcon', 'MP5',
-- 'SniperRifle',
-- 'AG36', 'OICW', 'P90', 'M4', 'Shotgun', 'M249', 'Commando',
-- 'Rocket', 'VehicleRocket', 'HandGrenade', 'StickExplosive',
-- 'Boat', 'Vehicle', 
-- 'VehicleMountedRocketMG', 'VehicleMountedAutoMG', 'MG',
-- 'VehicleMountedMG', 'OICWGrenade', 
-- 'AG36GrenadeBoat', 'Vehicle', 'VehicleMountedRocketMG',
-- 'VehicleMountedAutoMG',
-- 'MG', 'VehicleMountedMG', 'OICWGrenade', 'AG36Grenade')

select get_killer_class(weapon_code)
from match_frag
WHERE weapon_code is not null
LIMIT 48