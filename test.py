# from datetime import datetime, timezone, timedelta


# data = "Friday, November 09, 2018 12:22:07"
# format = "%A, %B %d, %Y %H:%M:%S"
# start_time = datetime.strptime(data, format)
# tz = timezone(timedelta(days=-1, seconds=68400))
# print(start_time)

# s = datetime(1,1,11,1,1,1, tzinfo=tz)
# print(s)

#wp9
# import csv
# with open('f.csv', 'w') as f:
#     writer = csv.writer(f)
#     writer.writerow(['Spam'] * 5 + ['Baked Beans'])
#     writer.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])

#wp25
import sqlite3
conn = sqlite3.connect('/home/tiit/farcry-data/farcry')

cursor = conn.execute("SELECT * from match")