# Random flights generator
Python script to generate random flights data.

## Table of Contents
* [General Info](#general-info)
* [Technologies Used](#technologies-used)
* [Setup](#setup)
* [Usage](#usage)

## General Info
I've created this script to generate flights because unfortunately no company provides for free REST API with flight data. I uses this generator in my [Flight search engine project](https://github.com/bladeours/flight-search-engine). It sends data by POST request directly to [Flight API](https://github.com/bladeours/flight-api). Generator uses [Airport API](https://github.com/bladeours/airport-api) to get distance between airports and calculate price and time utilizing how many kilometers there are.

## Technologies Used
* Python 3

## Setup
You need to run [Flight API](https://github.com/bladeours/flight-api) and [Airport API](https://github.com/bladeours/airport-api).
## Usage
`usage: generator.py --number <n> --ip_distance <ip_distance_api> --ip_flight <ip_flight_api> --environment`
* `<n>` number of flights you want to generate
* `<ip_distance_api>` ip of [Airport API](https://github.com/bladeours/airport-api)
* `<ip_flight_api>` ip of [Flight API](https://github.com/bladeours/flight-api)
* `--environment` use it if you want set rest parameters by environmental variables










