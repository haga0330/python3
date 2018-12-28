# coding: utf-8
"""Notification to slack."""

import json
import datetime
import os
import requests
import logging

# slack webhook url
slack_post_url = os.environ["webhook_1"]
# slack channel
slack_channel = os.environ["channel_1"]
# notify messages
notify_messages_1 = os.environ["message_1"]

dt_utc = datetime.datetime.now(tz=datetime.timezone.utc)
dt_jst = dt_utc + datetime.timedelta(hours=9)
dt_fm = "{0:%Y-%m-%d-%H:%M:%S}".format(dt_jst)

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """Notification content."""
    content = notify_messages_1 + " " + dt_fm
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
