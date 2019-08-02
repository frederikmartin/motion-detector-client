import sys
import os
import json
import requests

class LambdaClient:
    def __init__(self, base_url, logger):
        self.base_url = base_url
        self.api_key = os.environ['LAMBDA_API_KEY']
        self.logger = logger
    
    def notify_user(self):
        url = '{}'.format(self.base_url)
        headers = {
            'x-api-key': self.api_key
        }
        try:
            response = requests.post(url, headers=headers)
        except:
            e = sys.exc_info()[0]
            self.logger.error('Request failed: {}'.format(e))
        return response.json()
