from ast import arg, parse
from datetime import date, datetime
from sqlite3 import Timestamp
from turtle import distance
from progress.bar import Bar
from requests.adapters import HTTPAdapter, Retry
import requests
import random
import argparse
import time
import json
import os

def random_date(start,end):
    start_date_timestamp = datetime.timestamp(start)
    end_date_timestamp = datetime.timestamp(end)
    random_timestamp = random.uniform(start_date_timestamp, end_date_timestamp)
    random_date = datetime.fromtimestamp(random_timestamp)
    return random_date

parser = argparse.ArgumentParser(description='Generate random flights')
parser.add_argument('--number', '-n', help='number of rows')
parser.add_argument('--ip_distance', '-d', help='IP of distance API')
parser.add_argument('--ip_flight', '-f', help='IP of flight API')
parser.add_argument('--environment', '-e', help='Use environmental variables', action='store_true')
args = parser.parse_args()
if args.number:
    number_of_rows = int(args.number)
if args.ip_distance:
    ip_distance = args.ip_distance
else:
    ip_distance = "http://localhost:8081"

if args.ip_flight:
    ip_flight = args.ip_flight
else:
    ip_flight = "http://localhost:8082"

if args.environment:
    ip_flight = os.getenv("IP_FLIGHT")
    ip_distance = os.getenv("IP_DISTANCE")
    number_of_rows = int(os.getenv("ROWS"))

codes_array = []
with open("airports_codes.txt") as codes:
    for code in codes:
        codes_array.append(code.strip("\n"))

bar = Bar('Processing', max=number_of_rows)
for i in range(number_of_rows):
    bar.next()
    departure_airport = random.choice(codes_array)
    arrival_airport = random.choice(codes_array)
    while(departure_airport == arrival_airport):
        arrival_airport = random.choice(codes_array)
    departure_date = random_date(datetime.now(),datetime.strptime('2023-08-01 00:00:00',"%Y-%m-%d %H:%M:%S"))
    all_seats = random.randrange(40,400)
    free_seats = random.randrange(0,all_seats)
    company = random.randrange(1,73)
    s = requests.Session()
    retries = Retry(total=40, backoff_factor=0.1)
    s.mount('http://', HTTPAdapter(max_retries=retries))
    r = s.get("{}/distance/{}/{}".format(ip_distance, departure_airport, arrival_airport), timeout=(60 * 5))
    if r.status_code != 200:
        continue
    distance = r.json()['distance_km']
    
    if distance < 800:
        fligt_speed = 500
    else:
        fligt_speed = 800
    average_flight_time_seconds = (distance/fligt_speed) * 60 * 60
    flight_time_seconds = random.randrange((int)(0.9 * average_flight_time_seconds), (int)(1.1 * average_flight_time_seconds))
    flight_time = time.strftime('%H:%M:%S', time.gmtime(flight_time_seconds))

    if distance < 1000:
        price_converter = 0.05
    elif distance < 10000: 
        price_converter = 0.1
    else:
        price_converter = 0.4
    price_distance = distance * price_converter
    price = round(random.uniform(0.5 * price_distance, 1.5 * price_distance),2)

    r = s.get("{}/company/{}".format(ip_flight, company))
    company_json = r.json()
    
    r = s.get("{}/airport/raw/{}".format(ip_flight, departure_airport))
    departure_airport_json = r.json()

    r = s.get("{}/airport/raw/{}".format(ip_flight, arrival_airport))
    arrival_airport_json = r.json()


    flight_dict = {}
    flight_dict['departureAirport'] = departure_airport_json
    flight_dict['arrivalAirport'] = arrival_airport_json
    flight_dict['departureDate'] = int(datetime.timestamp(departure_date)*1000)
    flight_dict['flightTime'] = flight_time
    flight_dict['allSeats'] = all_seats
    flight_dict['freeSeats'] = free_seats
    flight_dict['price'] = price
    flight_dict['company'] = company_json
    flight_dict['distance_km'] = distance
    flight_json = json.dumps(flight_dict)

    r = s.post(ip_flight + "/flight", data = flight_json, headers={'Content-Type':'application/json'})
    
bar.finish()
print("Added {} flights to app.".format(number_of_rows))

