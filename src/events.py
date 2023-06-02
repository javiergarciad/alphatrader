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
        self.failed_deliveries = []
        self.logger = logging.getLogger("DataBus")

    def subscribe(self, callback):
        """
        Subscribe a callback function to receive data updates.

        Args:
        - callback: The callback function to be subscribed.
        """
        self.subscribers.append(callback)

    def publish(self, data):
        """
        Publish data to all subscribers.

        Args:
        - data: The data to be published.

        Exceptions:
        - Any exceptions raised during data delivery are caught and logged. Failed deliveries
          are stored in the 'failed_deliveries' list for retry.
        """
        for subscriber in self.subscribers:
            try:
                subscriber(data)
            except Exception as e:
                self.logger.error(f"Failed to deliver data to subscriber: {e}")
                self.failed_deliveries.append((subscriber, data))

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
