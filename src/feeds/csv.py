

import csv
import time
import redis

from src.feeds import DataFeed

class CSVDataHandler(DataFeed):
    def __init__(self, csv_file, redis_client, delay=1):
        self.csv_file = csv_file
        self.delay = delay
        self.data = []
        self.redis_client = redis_client


    

    def generate_data_feed(self):
        with open(self.csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                message = ','.join(row.values())
                yield message

    def publish_latest_price(self):
        for message in self.generate_data_feed():
            self.redis_client.publish('prices_feed', message)
            time.sleep(self.delay)  # Simulate data feed delay
