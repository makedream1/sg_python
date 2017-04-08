import argparse
import requests

API_KEY = "5ff6420f3b83035f456667a6dd60f3fa"
url = "http://api.openweathermap.org/data/2.5/weather?"


def parser_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--location', nargs='+')
    parser.add_argument('-i', '--id')
    return parser.parse_args()


if __name__ == "__main__":
    args = parser_args()
    if args.id:
        url_for_id = "{}id={}&appid={}".format(url, args.id, API_KEY)
        data = requests.get(url_for_id).json()
        json_object = data
        kel_temp = json_object['main']['temp']
        cel_temp = kel_temp - 273.15
        print("Current temp in {}: {}{} C".format(data['name'], int(cel_temp), chr(176)))

    if args.location:
        location_args = " ".join(args.location)
        url_for_location = "{}q={}&appid={}".format(url, location_args, API_KEY)
        data = requests.get(url_for_location).json()
        kel_temp = data['main']['temp']
        cel_temp = kel_temp - 273.15
        print("Current temp in {}: {}{} C".format(data['name'], round(cel_temp, 2), chr(176)))
