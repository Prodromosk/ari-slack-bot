from flask import Flask, render_template, request, flash, redirect, url_for, Markup
import os
from slack import WebClient
from slack.errors import SlackApiError
import datetime
import time
from time import sleep

client = WebClient(token=os.environ["SLACK_API_TOKEN"])
channel_to_listen = os.environ['CHANNEL_TO_LISTEN']

app = Flask(__name__)

# Custom template filter for UNIX timestamp conversion to readable Date
@app.template_filter('ctime')
def nix_timestamp_conversion(s):
    return time.ctime(float(s))

@app.route("/", methods=['GET', 'POST'])
def home():

    response = client.conversations_history(channel=channel_to_listen, limit=200)
    messages = response['messages']

    replies = []

    for message in messages:
        if 'thread_ts' in message:

            timestamp = message['thread_ts']
            convo_replies = client.conversations_replies(channel=channel_to_listen,
                                                        ts=timestamp,
                                                        latest='now')
            replies.append(convo_replies['messages'])
    assert response['ok']



    return render_template('index.html', messages=messages, replies=replies)

if __name__ == "__main__":
    app.run(use_reloader = True, debug = True)
