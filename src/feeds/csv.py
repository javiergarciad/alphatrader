

import csv

from src.feeds import DataFeed

class CSVDataHandler(DataFeed):
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.data = []

    def load_data(self):
        with open(self.csv_file, 'r') as file:
            reader = csv.DictReader(file)
            self.data = list(reader)

    def get_next(self):
        if not self.data:
            return None
        return self.data.pop(0)