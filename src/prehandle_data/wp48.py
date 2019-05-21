import psycopg2 

# Insert Game Session Data to PostgreSQL Database

def insert_match_to_postgresql(properties, start_time, end_time, game_mode, map_name, frags):
    '''
    @param: properties:  a tuple of the following form: (hostname, database_name, username, password)
    '''
    connection = psycopg2.connect(dbname=properties[1], user=properties[2], password=properties[3], host=properties[0])
    cursor = connection.cursor()
    cursor.execute("""
           INSERT INTO match (start_time, end_time, game_mode, map_name)
           VALUES (%s, %s, %s, %s)
           RETURNING match_id;
           """, (start_time, end_time, game_mode, map_name))
    
    insert_frags_to_postgres(connection, cursor.fetchone(), frags)

    connection.commit()
    cursor.close()
    connection.close()
    return id



def insert_frags_to_postgres(connection, match_id, frags):
    '''
    wp26
    '''
    beauty_frags = []
    for frag in frags:
        frag = (match_id, ) + frag
        substract = 5 - len(frag)
        if substract != 0:
            frag += (None,) * substract
        beauty_frags.append(frag)
        
    cursor = connection.cursor()
    cursor.executemany("""
            INSERT INTO match_frag (match_id, frag_time, killer_name, victim_name, weapon_code)
            VALUES (%s, %s, %s, %s, %s)
            """, beauty_frags)
    connection.commit()
    cursor.close()
    
    