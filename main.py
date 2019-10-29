import time
import requests
from influxdb import InfluxDBClient
import datetime
import logging
import os
CLIENT_ID = os.getenv("NETATMO_CLIENT_ID")
CLIENT_SECRET = os.getenv("NETATMO_CLIENT_SECRET")
NETATMO_USERNAME = os.getenv("NETATMO_USERNAME")
NETATMO_PASSWORD = os.getenv("NETATMO_PASSWORD")
INFLUXDB_HOST = os.getenv('INFLUXDB_HOST', "influxdb")
INFLUXDB_PORT = int(os.getenv('INFLUXDB_PORT', 8086))
INFLUXDB_DB = os.getenv('INFLUXDB_DB', "office")

_ALLOWED_TYPES = ('Temperature', 'CO2', 'Humidity', 'Pressure', 'AbsolutePressure', 'health_idx', 'Noise')


def get_access_token():
    '''
    returns:
     { access_token, expires_in, refresh_token }
    '''
    payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'password',
        'username': NETATMO_USERNAME,
        'password': NETATMO_PASSWORD,
        'scope': 'read_homecoach'
    }

    r = requests.post('https://api.netatmo.com/oauth2/token', data=payload)
    response = r.json()
    response['expires_at'] = time.time() + (response['expires_in'] / 2)

    return response


def refresh_token(token_info):
    '''
    returns:
     { access_token, expires_in, refresh_token }
    '''

    if token_info['expires_at'] > time.time():
        return token_info

    payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'refresh_token',
        'refresh_token': token_info['refresh_token']
    }

    r = requests.post('https://api.netatmo.com/oauth2/token', data=payload)
    response = r.json()
    response['expires_at'] = time.time() + (response['expires_in'] / 2)
    return response


def get_station_info(access_token):
    payload = {
        'access_token': access_token,
    }
    r = requests.get('https://api.netatmo.com/api/gethomecoachsdata', params=payload)
    return r.json()


def get_influxdb_client():
    client = InfluxDBClient(host=INFLUXDB_HOST, port=INFLUXDB_PORT)
    if {'name': INFLUXDB_DB} not in client.get_list_database():
        client.create_database(INFLUXDB_DB)
    client.switch_database(INFLUXDB_DB)
    return client


def iterate_stations(access_token, client):
    station_info = get_station_info(access_token)
    if 'body' not in station_info:
        raise Exception(station_info)
    stations = station_info['body']['devices']
    points = []
    for station in stations:
        logging.debug('Station :' + station['station_name'])
        time_metrics = datetime.datetime.utcfromtimestamp(station['dashboard_data']['time_utc']).isoformat()
        point = {
            "measurement": 'netatmo',
            "tags": {
                "station": station['station_name'],
            },
            "time": datetime.datetime.now().isoformat(),
            "fields": {}
        }
        fields = 0
        for substation, value in station['dashboard_data'].items():
            if substation in _ALLOWED_TYPES:
                point['fields'][substation] = float(value)
                fields = fields + 1
        if fields > 0:
            points.append(point)
            logging.info('%s appended %d fields last_updated %s', station['station_name'], fields, time_metrics)
    if len(points) > 0:
        client.write_points(points)
        logging.info("Saved to InfluxDb")


logging.basicConfig(level=logging.INFO)
token_info = get_access_token()
dbClient = get_influxdb_client()
while True:
    token_info = refresh_token(token_info)
    iterate_stations(token_info['access_token'], dbClient)
    time.sleep(10)
