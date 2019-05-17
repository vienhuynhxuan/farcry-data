from datetime import datetime, timedelta, timezone
import math
import re 


def read_log_file(log_file):
    with open(log_file) as file:
        return file.read()


def parse_log_start_time(log_data):
    log_data = log_data.split("\n")
    
    time_data = log_data[0]
    format_time = "%A, %B %d, %Y %H:%M:%S"
    start_time = datetime.strptime(time_data[len("Log Started at "):], format_time)
    # wp3: timezone
    timezone_data = list(filter(lambda x: "g_timezone" in x, log_data))[0]

    index_comma = timezone_data.index(",")
    timezone = timezone_data[index_comma + 1: -1]
    timezone = int(timezone)
    time_delta = timedelta(days= -1 if timezone < 0 else 0, seconds=abs(timezone) * 3600)
 
    time_zone = timezone(offsest=time_delta)
    print(time_zone)


def parse_match_mode_and_map(log_data):
    log_data = log_data.split("\n")
    data = list(filter(lambda x: "Loading level" in x, log_data))[0]
    data = data.split(" ")
    mode = data[-2]
    map = data[4].split("/")[1][:-1]
    return (mode, map)


def parse_frags(log_data):
    log_data = log_data.split("\n")

    flags =[]
    for row in log_data:
        row = row.split(" ")
        if len(row) == 7:
            if "killed" == row[3]:
                flag = (row[0][1:-1], row[2], row[4], row[6])
                flags.append(flag)
    return flags


def prettify_frags(frags):
    emoji = { 'killer': '😛', 'victem': '😧',
            'Vehicle': '🚙', 
            'Falcon':'🔫', 'Shotgun':'🔫', 'P90':'🔫', 
            'MP5':'🔫', 'M4':'🔫', 'AG36':'🔫', 'OICW':'🔫', 'SniperRifle':'🔫', 
            'M249':'🔫', 'VehicleMountedAutoMG':'🔫', 'VehicleMountedMG':'🔫',
            'HandGrenade':'💣', 'AG36Grenade':'💣', 'OICWGrenade':'💣', 'StickyExplosive':'💣',
            'Rocket':'🚀', 'VehicleMountedRocketMG':'🚀', 'VehicleRocket':'🚀',
            'Machete':'🔪',
            'Boat':'🚤',
    }
    prettified_flags = []
    for frag in frags:
        prettified_flags.append((frag[0] + emoji[killer] + frag[1] + emoji[frag[-1]]+ frag[-2])

    return prettify_frags

log_data = read_log_file("/home/tiit/farcry-data/farcry_data_science_introduction/logs/log01.txt")

print(parse_frags(log_data))