# coding: utf-8
"""Notification to slack."""

import json
import os
import requests
import logging

# slack webhook url
slack_post_url = os.environ["webhook_1"]
# slack channel
slack_channel = os.environ["channel_1"]
# Location(State)
state_city = os.environ["state"]

logger = logging.getLogger()
logger.setLevel(logging.INFO)

url = 'http://weather.livedoor.com/forecast/webservice/json/v1'
params = {'city': state_city}
res = requests.get(url, params=params)
json_data = res.json()


def lambda_handler(event, context):
    """Notification content."""
    title = json_data['title']
    weather = json_data['description']['text']
    publictime = json_data['description']['publicTime']
    content = title + " " + publictime + "\n" + weather
    # Message to slack.
    slack_message = {
        'channel': slack_channel,
        "text": content,
    }

    # Post to slack.
    try:
        req = requests.post(slack_post_url, data=json.dumps(slack_message))
        logger.info("Message posted to %s", slack_message['channel'])
    except requests.exceptions.RequestException as e:
        logger.error("Request failed: %s", e)
