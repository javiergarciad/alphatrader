import csv
from pathlib import Path
import time
from src.common.tools import get_project_root

from src.feeds import DataFeed
import logging
import redis

logger = logging.getLogger(__name__)


class CSVDataHandler(DataFeed):
    """
    A class for handling CSV data feed, providing historical market data for backtesting

    Args:
        csv_file (str): The path to the CSV file containing the historical or real-time data.
        ticket (str): The ticket or symbol representing the financial instrument.
        broker (str): The name of the broker or exchange providing the data.
        redis_client: The Redis client object for publishing data to the Redis server.
        delay (float, optional): The delay between publishing each data point (in seconds).
            Defaults to 1.

    Attributes:
        ticket (str): The ticket or symbol representing the financial instrument.
        broker (str): The name of the broker or exchange providing the data.
        csv_file (str): The path to the CSV file containing the data.
        delay (float): The delay between publishing each data point (in seconds).
        data (list): A list to store the data points read from the CSV file.
        redis_client: The Redis client object for publishing data to the Redis server.

    Methods:
        _get_data_type(header): Determines the type of data (candle or tick) based on the CSV header.
        generate_data_feed(): Generates a data feed by reading the CSV file and yielding data points.
        publish_latest_price(): Publishes each data point to the Redis server with a delay.

    Example Usage:
        redis_client = redis.Redis(host='localhost', port=6379)
        handler = CSVDataHandler('historical_data.csv', 'AAPL', 'XYZ Broker', redis_client)
        handler.publish_latest_price()
    """

    def __init__(self, csv_file, ticket, broker, redis_client, delay=1):
        self.ticket = ticket
        self.broker = broker
        self.csv_file = csv_file
        self.delay = delay
        self.data = []
        self.redis_client = redis_client

    def get_ticket(self):
        return self.get_ticket()

    def _get_data_type(self, header):
        lowercase_header = [col.lower() for col in header]
        if any(col in lowercase_header for col in ["open", "high", "low", "close"]):
            return "candle"
        elif any(col in lowercase_header for col in ["bid", "ask"]):
            return "tick"
        else:
            logger.error("Data can´t be identify as candle or tick")
            raise ValueError()

    def load_data(self):
        with open(self.csv_file, "r") as file:
            reader = csv.DictReader(file)
            header = reader.fieldnames
            data_type = self._get_data_type(header)

            for row in reader:
                message = {
                    "ticket": self.ticket,
                    "broker": self.broker,
                    "data_type": data_type,
                }
                for col in header:
                    # handle both candles or ticks
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

    def publish_latest_price(self):
        """
        Publishes each data point to the Redis server with a delay.

        Returns:
            None
        """
        for message in self.load_data():
            self.redis_client.publish("prices_feed", message)
            time.sleep(self.delay)  # Simulate data feed delay


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    redis_client = redis.Redis(
        host="localhost",
        port=6379,
    )
    csv_file = Path(get_project_root(), "data", "AAPL.csv")
    handler = CSVDataHandler(csv_file, "AAPL", "XYZ Broker", redis_client)
    handler.publish_latest_price()
