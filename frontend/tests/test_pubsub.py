import pytest
import json

def test_redis_connection(redis):
    assert redis.ping()

def test_redis_subscribe(redis):
    pubsub = redis.pubsub()
    pubsub.subscribe('book_updates')
    message = pubsub.get_message(timeout=1)
    assert message is not None
    assert message['type'] == 'subscribe' 