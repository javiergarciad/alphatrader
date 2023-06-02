import logging

class DataBus:
    """
    In-memory data bus for publishing and subscribing to data updates.

    This implementation is suitable for in-memory communication within a single program
    or process. If you need to communicate between multiple processes or across
    multiple machines, consider using a distributed data bus like Redis, RabbitMQ or Kafka.
    """

    def __init__(self):
        """
        Initialize the DataBus.

        Attributes:
        - subscribers: A list to hold the subscribed callback functions.
        - failed_deliveries: A list to store failed data deliveries for retry.
        - logger: A logger object for logging errors and messages.
        """
        self.subscribers = []
        self.channels = []
        self.failed_deliveries = []
        self.logger = logging.getLogger("DataBus")

    def subscribe(self, channel, subscriber):
        """
        Subscribes a subscriber to a specific channel.

        Args:
            channel (str): The name of the channel.
            subscriber (callable): The subscriber function or object.

        Returns:
            None
        """
        if channel not in self.channels:
            self.channels[channel] = []

        if subscriber not in self.channels[channel]:
            self.channels[channel].append(subscriber)
        else:
            logging.warning(f"Subscriber already exists in channel: {channel}")



    def publish(self, channel, data):
        """
        Publishes data to a specific channel, notifying all subscribers.

        Args:
            channel (str): The name of the channel.
            data: The data to be published.

        Returns:
            None
        """
        if channel in self.channels:
            for subscriber in self.channels[channel]:
                try:
                    subscriber(data)
                except Exception as e:
                    logging.error(f"Error while publishing data to {channel}: {e}")
        else:
            logging.warning(data)
            # logging.warning(f"No subscribers found for channel: {channel}")


    def retry_failed_deliveries(self):
        """
        Retry failed data deliveries.

        Exceptions:
        - Any exceptions raised during retry are caught and logged.
        """
        for subscriber, data in self.failed_deliveries:
            try:
                subscriber(data)
                self.failed_deliveries.remove((subscriber, data))
            except Exception as e:
                self.logger.error(f"Failed to retry delivery to subscriber: {e}")

    def get_failed_deliveries(self):
        """
        Get a list of failed deliveries.

        Returns:
        - A list of tuples containing the subscriber and data of failed deliveries.
        """
        return self.failed_deliveries
