from datetime import datetime, timedelta, timezone
import math
import re 
import csv


def read_log_file(log_file):
    """
    wp1
    """
    with open(log_file) as file:
        return file.read()


def parse_log_start_time(log_data):
    """
    wp2
    wp3
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
    time_delta = timedelta(days= -1 if time_zone < 0 else 0, seconds=abs(time_zone) * 3600) 
    time_zone = timezone(time_delta)
    start_time = datetime(start_time.year, start_time.month, start_time.day, start_time.hour, start_time.minute, start_time.second, tzinfo = time_zone)

    return start_time


def parse_match_mode_and_map(log_data):
    """
    wp4
    """

    log_data = log_data.split("\n")
    data = list(filter(lambda x: "Loading level" in x, log_data))[0]
    data = data.split(" ")
    mode = data[-2]
    map = data[4].split("/")[1][:-1]
    return (mode, map)


def parse_frags(log_data):
    '''
    wp5
    <35:36> <Lua> cyap killed Jack The Ripper with AG36Grenade
    ex:     <35:36> <Lua> cyap killed killed Jack The Ripper with AG36Grenade
    wp6
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
    wp7
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


def write_frag_csv_file(log_file_pathname, frags):
    with open(log_file_pathname, 'w') as csv_file:
        writer = csv.writer(csv_file)
        for frag in frags:
            frag = list(frag)
            time = [str(frag[0])]
            writer.writerow(time + frag[1:])



log_data = read_log_file('/home/tiit/farcry-data/farcry_data_science_introduction/logs/log04.txt')
frags = parse_frags(log_data)
write_frag_csv_file('./log04.csv', frags)