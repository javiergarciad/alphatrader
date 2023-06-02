import csv
from pathlib import Path
import time
from src.common.tools import get_project_root
from src.events import DataBus

from src.feeds import DataFeed
import logging


logger = logging.getLogger(__name__)


class CSVDataHandler(DataFeed):
    """
    A class for handling CSV data feed, providing historical market data for backtesting.

    Args:
        csv_file (str): The path to the CSV file containing the historical or real-time data.
        ticket (str): The ticket or symbol representing the financial instrument.
        broker (str): The name of the broker or exchange providing the data.
        data_bus: In-memory data bus for storing and retrieving data.
        delay (float, optional): The delay between publishing each data point (in seconds).
            Defaults to 1.

    Attributes:
        ticket (str): The ticket or symbol representing the financial instrument.
        broker (str): The name of the broker or exchange providing the data.
        csv_file (str): The path to the CSV file containing the data.
        delay (float): The delay between publishing each data point (in seconds).
        data_bus (DataBus): In-memory data bus for storing and retrieving data.

    Methods:
        _get_data_type(header): Determines the type of data (candle or tick) based on the CSV header.
        load_data(): Loads the data from the CSV file.
        deliver_prices(): Delivers each price from the oldest to the newest with a 1-second delay.
        publish_price(price): Publishes a price to the data bus.

    Example Usage:
        data_bus = DataBus()
        handler = CSVDataHandler('historical_data.csv', 'AAPL', 'XYZ Broker', data_bus)
        handler.deliver_prices()
    """

    def __init__(self, csv_file, ticket, data_bus, delay=1):
        self.ticket = ticket
        self.csv_file = csv_file
        self.delay = delay
        self.data_bus = data_bus

    def get_ticket(self):
        return self.ticket

    def _get_data_type(self, header):
        lowercase_header = [col.lower() for col in header]
        if any(col in lowercase_header for col in ["open", "high", "low", "close"]):
            return "candle"
        elif any(col in lowercase_header for col in ["bid", "ask"]):
            return "tick"
        else:
            raise ValueError("Data cannot be identified as candle or tick")

    def load_data(self):
        with open(self.csv_file, "r") as file:
            reader = csv.DictReader(file)
            header = reader.fieldnames
            data_type = self._get_data_type(header)

            for row in reader:
                message = {
                    "ticket": self.ticket,
                    "data_type": data_type,
                }
                for col in header:
                    if col.lower() in [
                        "date",
                        "datetime",
                        "bid",
                        "ask",
                        "open",
                        "high",
                        "low",
                        "close",
                        "adj close",
                        "volume",
                    ]:
                        message[col.lower()] = row[col]

                yield message

    def run(self):
        """
        Delivers each price from the oldest to the newest with a delay.

        Returns:
            None
        """
        for price in self.load_data():
            self.data_bus.publish("prices", price)
            time.sleep(self.delay)




if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    data_bus = DataBus()
    csv_file = Path(get_project_root(), "data", "AAPL.csv")
    handler = CSVDataHandler(csv_file, "AAPL", data_bus)
    handler.run()
