import os
from slack import WebClient
from slack.errors import SlackApiError
import datetime

client = WebClient(token=os.environ["SLACK_API_TOKEN"])
channel_to_listen = os.environ['CHANNEL_TO_LISTEN']

def main():
    response = client.conversations_history(channel=channel_to_listen, limit=3)
    messages = response['messages']
    replies = []

    assert response['ok']

    for message in messages:
        timestamp = message['ts']
        convo_replies = client.conversations_replies(channel=channel_to_listen,
                                                    ts=timestamp,
                                                    latest='now')
        replies.append(convo_replies['messages'])
        # replies = convo_replies['messages']
        print(replies, '\n\n')



if __name__ == '__main__':
    main()



# print(response['messages'][0]['text'])
# print(messages_only['messages'][0]['text'][0])
