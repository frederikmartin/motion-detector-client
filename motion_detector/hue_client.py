import sys
import json
import requests
from datetime import datetime

class HueClient:
    def __init__(self, base_url, user, motion_sensor, logger):
        self.base_url = base_url
        self.user = user
        self.motion_sensor = motion_sensor
        self.logger = logger
    
    def query_sensor_data(self):
        url = 'http://{}/api/{}/sensors/{}'.format(self.base_url, self.user, self.motion_sensor)
        try:
            response = requests.get(url)
            motion_detected, last_updated = response.json()['state']['presence'], response.json()['state']['lastupdated']
        except:
            e = sys.exc_info()[0]
            self.logger.error('Request failed: {}'.format(e))
        return motion_detected, datetime.strptime(last_updated, '%Y-%m-%dT%H:%M:%S')
