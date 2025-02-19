import pytest
import json

def test_redis_connection(redis):
    assert redis.ping()

def test_redis_publish(redis):
    test_data = {
        'action': 'add',
        'book': {
            'id': 1,
            'title': 'Test Book',
            'publisher': 'Test Publisher',
            'category': 'Test'
        }
    }
    result = redis.publish('book_updates', json.dumps(test_data))
    assert result >= 0  # Returns number of clients that received the message 