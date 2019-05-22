
drop function if exists a;

drop table if exists temp;
create table temp(
    killer_name text,
    kill_count int
);


insert into temp(killer_name, kill_count) values ('hello', 123);
insert into temp(killer_name, kill_count) values ('hello', 1234);


create function a(x int)
returns table(killer_name text, kill_count int) as $$
DECLARE cur CURSOR
FOR 
  SELECT * FROM temp;
a text;
b int;
BEGIN
  OPEN cur;

  LOOP
    FETCH cur INTO a, b; 
    EXIT WHEN NOT FOUND; 
    return query select * from temp;
  
  END LOOP;
end;
$$
LANGUAGE plpgsql;


select a(31);
