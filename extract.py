import os
import slack
from slack import WebClient
import json
from time import sleep
import pandas as pd

CHANNEL = os.environ['CHANNEL_TO_LISTEN']
MESSAGES_PER_PAGE = 200
MAX_MESSAGES = 10000

# init web client
client = WebClient(token=os.environ["SLACK_API_TOKEN"])

# get first page
page = 1
print("Retrieving page {}".format(page))
response = client.conversations_history(
    channel=CHANNEL,
    limit=MESSAGES_PER_PAGE,
)
assert response["ok"]
messages_all = response['messages']

# get additional pages if below max message and if they are any
while len(messages_all) + MESSAGES_PER_PAGE <= MAX_MESSAGES and response['has_more']:
    page += 1
    print("Retrieving page {}".format(page))
    sleep(1)   # need to wait 1 sec before next call due to rate limits
    response = client.conversations_history(
        channel=CHANNEL,
        limit=MESSAGES_PER_PAGE,
        cursor=response['response_metadata']['next_cursor']
    )
    assert response["ok"]
    messages = response['messages']
    messages_all = messages_all + messages

print(
    "Fetched a total of {} messages from channel {}".format(
        len(messages_all),
        CHANNEL
))

replies = []

for message in messages_all:
    if 'thread_ts' in message:

        timestamp = message['thread_ts']
        convo_replies = client.conversations_replies(channel=CHANNEL,
                                                    ts=timestamp,
                                                    latest='now')
        replies.append(convo_replies['messages'])

# Convert extract to csv
def convert_json_to_csv():
    df = pd.read_json (r'extract.json')
    df.to_csv (r'extract.csv', index = None)

# write the result to a file
with open('extract.json', 'w', encoding='utf-8') as f:
  json.dump(
      replies,
      f,
      sort_keys=True,
      indent=4,
      ensure_ascii=False
    )
convert_json_to_csv()
