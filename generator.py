from ast import arg, parse
from datetime import date, datetime
from sqlite3 import Timestamp
from turtle import distance
import requests
import random
import argparse
import time

def random_date(start,end):
    start_date_timestamp = datetime.timestamp(start)
    end_date_timestamp = datetime.timestamp(end)
    random_timestamp = random.uniform(start_date_timestamp,end_date_timestamp)
    random_date = datetime.fromtimestamp(random_timestamp)
    return random_date

parser = argparse.ArgumentParser(description='Generate random flights')
parser.add_argument('--number','-n',help='number of rows', required=True)
parser.add_argument('--ip','-i',help='IP of API')
args = parser.parse_args()

number_of_rows = int(args.number)
# number_of_rows = 1
codes_array = []

with open("airports_codes.txt") as codes:
    for code in codes:
        codes_array.append(code.strip("\n"))

sql_file = open("insert_fligts.sql","w")
sql_file.truncate(0)

for i in range(number_of_rows):
    departure_airport = random.choice(codes_array)
    arrival_airport = random.choice(codes_array)
    while(departure_airport == arrival_airport):
        arrival_airport = random.choice(codes_array)
    
    departure_date = random_date(datetime.now(),datetime.strptime('2023-08-01 00:00:00',"%Y-%m-%d %H:%M:%S"))
   
    flight_time_seconds = random.randrange(60*40,60*60*10)
    flight_time = time.strftime('%H:%M:%S', time.gmtime(flight_time_seconds))
   
    all_seats = random.randrange(40,400)

    free_seats = random.randrange(0,all_seats)

    price = round(random.uniform(25,2000),2)

    company = random.randrange(1,73)
   
    r = requests.get("http://localhost:8081/distance/{}/{}".format(departure_airport,arrival_airport))
    distance = r.json()['distance_km']

    print(departure_airport," -> ",arrival_airport, departure_date, flight_time, all_seats, free_seats, price, company, distance, "km")
    sql ="INSERT INTO flight(departure_airport, arrival_airport, departure_date, flight_time, all_seats, free_seats, price, company, distance) "
    sql = sql + ("VALUES('{}','{}','{}','{}',{},{},{},{},{});\n".format(departure_airport, arrival_airport, departure_date, flight_time, all_seats, free_seats, price, company, distance))
    
    sql_file.write(sql)

sql_file.close()


