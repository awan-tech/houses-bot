'''This is a script of a slack bot'''
import os
from pathlib import Path
import slack
from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
import mysql.connector
from parameter_store import para_store
from nearby import get_nearby
from geo import get_geo
from map import get_map



env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
app = Flask(__name__)
Slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRETS'], '/slack/events', app)
BOT_ID = client.api_call('auth.test')['user_id']
user_states = {}

'''Introduction of bot's commands'''
@app.route('/commands', methods=['POST'])
def commands():
    data = request.form
    channel_id = data.get('channel_id')
    client.chat_postMessage(channel=channel_id, text =
    '''
    Thank you for using Seal-Bot :kiss:

    Type 'nb' and start searching!
                            
    Not satisfied? I don't give a shit :kiss:
                            ''')
    return Response(), 200

@Slack_event_adapter.on('message')
def maps(payload):
    event = payload.get('event', {})
    user_id = event.get('user')

    if BOT_ID != user_id:
        channel_id = event.get('channel')
        user_text = event.get('text')
          
        if user_text == 'nb':
            user_states[user_id]='waiting'
            client.chat_postMessage(channel=channel_id, text =
                                    '''
                                    Enter an address or a zip code
I'll provide the map of 10 hotel that are nearest to you:smile:''')
            
        elif user_states.get(user_id) == 'waiting':
            try:
                client.files_upload(
                channels=channel_id,
                file=get_map(user_text)
                )
            except:
                client.chat_postMessage(channel=channel_id, text = 'Data not found')
            user_states.pop(user_id, None)

if __name__ == '__main__':
    app.run(debug=True,port=80)
