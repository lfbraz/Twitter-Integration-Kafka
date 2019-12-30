import logging
import settings as config
import time

# Library from Microsoft (https://github.com/Azure/azure-event-hubs-for-kafka)
from azure.eventhub import EventHubClient, Receiver

# Library from Confluent (https://github.com/confluentinc/confluent-kafka-python)
from confluent_kafka import Consumer


class CollectMessages():
    """
    Collect messages from streaming platforms
    """
    def GetMessagesFromEventHub():
        """
        Get messages from EventHub using azure.eventhub library
        """
        total = 0

        client = EventHubClient(config.EVENTHUB_ADDRESS,
                                debug=False,
                                username=config.EVENTHUB_USER,
                                password=config.EVENTHUB_KEY)

        try:
            receiver = client.add_receiver(
                config.EVENTHUB_CONSUMER_GROUP,
                config.EVENTHUB_PARTITION,
                prefetch=5000,
                offset=config.EVENTHUB_OFFSET)

            client.run()
            start_time = time.time()

            for event_data in receiver.receive(timeout=100):
                print("Received: {} \n".format(event_data.body_as_str(
                                                encoding='UTF-8')))
                total += 1

            end_time = time.time()
            client.stop()
            run_time = end_time - start_time
            print("Received {} messages in {} seconds".format(total, run_time))

        except KeyboardInterrupt:
            pass
        finally:
            client.stop()

    def GetMessagesFromKafka():
        """
        Get messages from Kafka (or Eventhub mode Kafka)
        using confluent_kafka library
        """
        # Create consumer
        c = Consumer(config.KAFKA)

        topics = [config.EVENTHUB_NAME]

        # Subscribe to topics
        c.subscribe(topics)

        while True:
            msg = c.poll(config.TIME_TO_WAIT)

            if msg is None:
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue

            print('Received message: {}'.format(msg.value().decode('utf-8')))

        c.close()
