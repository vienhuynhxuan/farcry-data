DROP TABLE temp;

create table temp(
    match_id uuid,
    killer_name text,
    kill_count int
);


CREATE OR REPLACE FUNCTION calculate_lucky_luke_killers(
    p_min_kill_count int default 3,
    p_max_time_between_kills int default 10
)
RETURNS void
AS $$
DECLARE
    match_id UUID;
    killer_name TEXT;
    kill_count INT default 0;

    rec_last_frag RECORD;
    rec_frag RECORD;
    cur CURSOR(p_min_kill_count_s int)
    FOR
        select *
        from 
            (select
                count(victim_name) over (
                    PARTITION BY match_id, killer_name
                ) kill_count, match_id, frag_time, killer_name, victim_name
            from 
                match_frag) as a
        where kill_count > p_min_kill_count_s;             
BEGIN
        
    OPEN cur(p_min_kill_count);
    m cur INTO rec_last_frag;
    LOOP
        EXIT WHEN NOT FOUND; --exit when table has no row       
        FETCH cur INTO rec_frag;

        IF (rec_frag.match_id = rec_last_frag.match_id AND rec_frag.killer_name = rec_last_frag.killer_name)
        THEN
            match_id := rec_frag[0];          
            killer_name := rec_frag[2];
            kill_count := kill_count + 1;  
        ELSE
            INSERT INTO temp values (match_id, killer_name, kill_count) ;
        END IF;


        FETCH cur INTO rec_last_frag;
    END LOOP;

    CLOSE cur;


END; $$
LANGUAGE PLPGSQL;


DO $$
BEGIN
PERFORM calculate_lucky_luke_killers(2,2);
END $$;
