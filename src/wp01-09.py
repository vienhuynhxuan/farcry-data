from datetime import datetime, timedelta, timezone
import math
import re 
import csv

def read_log_file(log_file_pathname):
    """
    Read Game Session Log File

    @param:  log_file_pathname: the pathname of a Far Cry server log file
    @return:    all the bytes from the file
    """
    with open(log_file_pathname) as file:
        return file.read()


def parse_log_start_time(log_data):
    """
    Parse Far Cry Engine's Start Time with Time Zone

    @param: log_data: data read from a Far Cry server's log file
    @return:    a datetime.datetime object representing the time with time zone infomation the Far Cry engine began to log events.
    """
    log_data = log_data.split("\n") #should optimize, iterator by hand to get first line.

    time_data = log_data[0]
    format_time = "%A, %B %d, %Y %H:%M:%S"
    start_time = datetime.strptime(time_data[len("Log Started at "):], format_time)
    # wp3: timezone
    timezone_data = list(filter(lambda x: "g_timezone" in x, log_data))[0]

    index_comma = timezone_data.index(",")
    time_zone = timezone_data[index_comma + 1: -1]
    time_zone = int(time_zone)
    if time_zone < 0:
        days = -1    
        seconds = (24 + time_zone) * 3600
    else:
        days = 0
        seconds = time_zone * 3600

    time_delta = timedelta(days=days, seconds=seconds) 
    time_zone = timezone(time_delta)

    start_time = datetime(start_time.year, start_time.month, start_time.day, start_time.hour, start_time.minute, start_time.second, tzinfo = time_zone)

    return start_time


def parse_match_mode_and_map(log_data):
    """
    Parse Match Session's Mode and Map

    @param: log_data: data read from a Far Cry server's log file
    @return:    a tuple (mode, map)
    """

    log_data = log_data.split("\n")
    data = list(filter(lambda x: "Loading level" in x, log_data))[0]
    data = data.split(" ")
    mode = data[-2]
    map = data[4].split("/")[1][:-1]
    return (mode, map)


def parse_frags(log_data):
    '''
    Parse Frag History

    @param: log_data: data read from a Far Cry server's log file
    @return a list of frags:
        Each frag is represented by a tuple in the following form:
        (frag_time, killer_name, victim_name, weapon_code)
        or, a simpler form, if the player committed suicide:
        (frag_time, killer_name)
    '''
    start_time = parse_log_start_time(log_data)
    log_data = log_data.split("\n")

    frags =[]
    for row in log_data:
        row = row.split(" ")
        if len(row) > 3 and "killed" == row[3]:
            time = row[0][1:-1].split(":")
            start_time_frag = start_time.replace(minute=int(time[0]), second=int(time[1]))
 
            frag = (start_time_frag, row[2])
            if "with" == row[-2]:
                frag += (row[4], row[6])

            frags.append(frag)
    return frags


def prettify_frags(frags):
    '''
    Prettify Frag History
    
    @param: frags: array of tuples of frags parsed from a Far Cry server's log file
    @return:    a list of strings by emoji,
    '''
    emoji = { 'killer': '😛', 'victem': '😧',
            'Vehicle': '🚙', 
            'Falcon':'🔫', 'Shotgun':'🔫', 'P90':'🔫', 'MG':'🔫',
            'MP5':'🔫', 'M4':'🔫', 'AG36':'🔫', 'OICW':'🔫', 'SniperRifle':'🔫', 
            'M249':'🔫', 'VehicleMountedAutoMG':'🔫', 'VehicleMountedMG':'🔫',
            'HandGrenade':'💣', 'AG36Grenade':'💣', 'OICWGrenade':'💣', 'StickyExplosive':'💣',
            'Rocket':'🚀', 'VehicleMountedRocketMG':'🚀', 'VehicleRocket':'🚀',
            'Machete':'🔪',
            'Boat':'🚤',
            'suicide': '@@'
    }

    prettified_flags = []
    for frag in frags:
        if len(frag) == 2:
            prettified_flags.append((frag[0] + " " + emoji['victem'] + " " + frag[1] + " " + emoji['suicide']))
        else:
            prettified_flags.append((frag[0] + " " + emoji['killer'] + " " + emoji[frag[-1]] + " " + emoji["victem"] + " " + frag[-2]))

    return prettified_flags


def parse_game_session_start_and_end_times(log_data, accept_corrupted=False):
    '''
    Determine Game Session's Start and End Times

    @param: log_data: data read from a Far Cry server's log file
    @param: accept_corrupted: if value is False, it means doesn't accept this log file as the game session has been somewhat corrupted and conversely
    @return:    approximate start and end time of the game session
    '''
    session_start_time = parse_log_start_time(log_data) #    wp8: optimize: get starttime after find corrupted

    log_data = log_data.split("\n")
    corrupted_row = [row for row in log_data if row.endswith('ERROR: $3#SCRIPT ERROR File: =C, Function: _ERRORMESSAGE,') ]

    if accept_corrupted is False and len(corrupted_row) == 1:
        return ()

    if len(corrupted_row) != 0:
        minute_second_end_time = corrupted_row[0][1:6]
    else:
        signal_statistic = "== Statistics                         \
                                                      \
                                      =="
        index_statistic_row = [index for index in range(len(log_data))
                               if log_data[index].endswith(signal_statistic)]
        minute_second_end_time = log_data[index_statistic_row[0] - 1][1:6]

    minute_end_time = int(minute_second_end_time[0:2])
    second_end_time = int(minute_second_end_time[3:5])
    session_end_time = session_start_time.replace(minute=minute_end_time,
                                                  second=second_end_time)

    return (session_start_time, session_end_time)


def write_frag_csv_file(log_file_pathname, frags):
    '''
    Create Frag History CSV File

    @param: log_file_pathname: pathname of the CSV file to store the frags in
    @param: frags: an array of tuples of the frags
    '''
    with open(log_file_pathname, 'w') as csv_file:
        writer = csv.writer(csv_file)
        for frag in frags:
            frag = list(frag)
            time = [str(frag[0])]
            writer.writerow(time + frag[1:])

log_data = read_log_file('/home/tiit/farcry-data/farcry_data_science_introduction/logs/log01.txt')
log_start_time = parse_log_start_time(log_data)
game_mode, map_name = parse_match_mode_and_map(log_data)
frags = parse_frags(log_data)
start_time, end_time = parse_game_session_start_and_end_times(log_data, False)

