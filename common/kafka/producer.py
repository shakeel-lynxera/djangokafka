"""
Generic Event Generators for CREATE, UPDATE and DELETE operations.
All system wide events are to be generated using these generic event
generators

"""
import logging
from json import dumps
from kafka import KafkaProducer
from djangokafka.settings import (
    KAFKA_EVENTS_TOPIC,
    KAFKA_EVENTS_BROKER,
    KAFKA_PRODUCE_EVENTS,
    SERVICE_NAME,
    KAFKA_PRODUCER_SEND_RETRIES,
)

# Get logger
logger = logging.getLogger(__name__)


# Supported Operation Types
class OperationTypes:
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


def generate_model_event(instance=None, serializer=None, operation=None):
    """Creates and publishes/produces a model event to the kafka events
       topic (configured in settings.py) with given operation type.

    model_event = {
        "source": "service.users",
        "event_type": "model",
        "operation": "create/update/delete",

        # event name format is fixed. "[operation]_[instance model name]"
        "event_name": "create_Role",

        "instance": {
            (serialized object being created)
        }
    }

    Args:
        instance ([django.db.models]): [The object being created]
        serializer ([restframework.serializers.ModelSerializer]): [Serializer
                                                            for the instance]
        operation ([Str]): [The operation performed on the instance
                            (create/update/delete)]
    """

    # Do not generate events if kafka disabled in settings
    if not KAFKA_PRODUCE_EVENTS:
        return

    if not operation:
        raise ValueError("publish event 'operation' not provided")

    if operation not in ["create", "update", "delete"]:
        raise ValueError("operation type '" + operation + "' not supported")

    # if not serializer:
    #     raise ValueError("publish event 'serializer' not provided for instance")

    if not instance:
        raise ValueError("publish event 'instance' is required")

    if serializer:
        event = {
            "source": SERVICE_NAME,
            "event_type": "model",
            "operation": operation,
            # event name format is fixed. "[operation]_[instance model name]"
            # e.g. create_Role
            "event_name": operation + "_" + type(instance).__name__,
            "instance": serializer(instance).data,
        }
    else:
        event = {
            "source": SERVICE_NAME,
            "event_type": "model",
            "operation": operation,
            # event name format is fixed. "[operation]_[instance model name]"
            # e.g. create_Role
            "event_name": operation + "_" + type(instance).__name__,
            "instance": instance,
        }

    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_EVENTS_BROKER],
        value_serializer=lambda x: dumps(x).encode("utf-8"),
        retries=KAFKA_PRODUCER_SEND_RETRIES,
    )

    def on_send_error():
        """Callback for error on sending event to topic"""
        logger.error("Event sending failed." + str(event))

    producer.send(KAFKA_EVENTS_TOPIC, value=event).add_errback(on_send_error)


def generate_auth_event(auth_event_name, event_data=None):
    """Publishes a custom authentication related event to the kafka events
    topic configured in settings

    auth_event = {
        "source": "service.users",
        "event_type": "auth",
        "event_name": "login/logout",
        "event_data": {
            (auth related data that needs to be passed with event)
        }
    }

    """

    # Do not generate events if kafka disabled in settings
    if not KAFKA_PRODUCE_EVENTS:
        return

    if not event_data:
        raise ValueError("event_data is required")

    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_EVENTS_BROKER],
        value_serializer=lambda x: dumps(x).encode("utf-8"),
        retries=KAFKA_PRODUCER_SEND_RETRIES,
    )

    def on_send_error():
        """Callback for error on sending event to topic"""
        logger.error("Event sending failed." + str(event))

    event = {
        "source": SERVICE_NAME,
        "event_type": "auth",
        "event_name": auth_event_name,
        "event": event_data,
    }

    producer.send(KAFKA_EVENTS_TOPIC, value=event).add_errback(on_send_error)


def generate_custom_model_event(event_name, event_data=None, operation=None):
    """Creates and publishes/produces a model event to the kafka events
       topic (configured in settings.py) with given operation type.

    model_event = {
        "source": "service.users",
        "event_type": "model",
        "operation": "create/update/delete",

        # event name format is fixed. "[operation]_[instance model name]"
        "event_name": "create_Role",

        "instance": {
            (serialized object being created)
        }
    }

    Args:
        instance ([django.db.models]): [The object being created]
        serializer ([restframework.serializers.ModelSerializer]): [Serializer
                                                            for the instance]
        operation ([Str]): [The operation performed on the instance
                            (create/update/delete)]
    """

    # Do not generate events if kafka disabled in settings
    if not KAFKA_PRODUCE_EVENTS:
        return

    if operation not in ["create", "update", "delete"]:
        raise ValueError("operation type '" + operation + "' not supported")

    event = {
        "source": SERVICE_NAME,
        "event_type": "custom_model",
        "operation": operation,
        "event_name": event_name,
        "event": event_data,
    }

    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_EVENTS_BROKER],
        value_serializer=lambda x: dumps(x).encode("utf-8"),
        retries=KAFKA_PRODUCER_SEND_RETRIES,
    )

    def on_send_error():
        """Callback for error on sending event to topic"""
        logger.error("Event sending failed." + str(event))

    print(producer.send(KAFKA_EVENTS_TOPIC, value=event).add_errback(on_send_error))
    print("Event data : ", event)
