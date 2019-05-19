import sqlite3


def insert_match_to_sqlite(file_pathname, start_time, end_time, game_mode, map_name, frags):
    '''
    wp25
    '''
    conn = sqlite3.connect(file_pathname)
    cursor = conn.cursor()

    cursor.execute('INSERT INTO match (start_time, end_time, game_mode, map_name) VALUES (?, ?, ?, ?)', (start_time, end_time, game_mode, map_name))

    insert_frags_to_sqlite(conn, cursor.lastrowid, frags)    

    conn.commit()
    conn.close()


def insert_frags_to_sqlite(connection, match_id, frags):
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
    cursor.executemany("INSERT INTO match_flag (match_id, frag_time, killer_name, victim_name, weapon_code) VALUES (?, ?, ?, ?, ?)", beauty_frags)  
        