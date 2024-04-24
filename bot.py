'''This is a script of a slack bot'''
import os
from pathlib import Path
import slack
from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
import mysql.connector
from parameter_store import para_store

env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

app = Flask(__name__)
Slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRETS'], '/slack/events', app)
BOT_ID = client.api_call('auth.test')['user_id']
user_states = {}

PARA_HOST = 'Host_name'
PARA_DB = 'DB_name'
PARA_USER = 'User_name'
PARA_PASSWORD = 'Password'
connection = mysql.connector.connect(host=para_store(PARA_HOST),
                                        database=para_store(PARA_DB),
                                        user=para_store(PARA_USER),
                                        password=para_store(PARA_PASSWORD))
cursor = connection.cursor()

'''Introduction of bot's commands'''
@app.route('/commands', methods=['POST'])
def commands():
    data = request.form
    channel_id = data.get('channel_id')
    user_id = data.get('user_id')
    client.chat_postMessage(channel=channel_id, text =
    '''
    Thank you for using Seal-Bot :kiss:
    This bot is used to get the amount of houses
    Followings are commands to trigger the bot, just type the command in your chatbox and send 
                            
    Filter by house type: ht
    Filter by price: pr
    Filter by avaliable date: ad
                            
    Not satisfied? I don't give a shit :kiss:
                            ''')
    return Response(), 200





@Slack_event_adapter.on('message')
def count(payload):
    event = payload.get('event', {})
    user_id = event.get('user')
    state = user_states.get(user_id, None)

    if BOT_ID != user_id:
        channel_id = event.get('channel')
        user_text = event.get('text')

        if user_text == 'ad':
           user_states[user_id] = 'ad'
           client.chat_postMessage(channel=channel_id, text =
        ''' Type the range or date u r looking for.
            (Example: 2023-3-15~2024-3-15) 
            ''')

        elif user_states.get(user_id) == 'ad':
            user_text = event.get('text')  
            if '~' in user_text:
                range_parts = user_text.split('~')
                try:
                    date1 = str(range_parts[0].strip())
                    date2 = str(range_parts[1].strip())
                    QUERY = '''SELECT COUNT(*) FROM houses
                    WHERE dates BETWEEN %s AND %s;
                    '''
                    cursor.execute(QUERY, (date1,date2,))
                    result = cursor.fetchone()
                    result = list(result)[0]
                    client.chat_postMessage(channel=channel_id, text = f'There are {result} left.')
                    user_states.pop(user_id, None)
                except :
                    client.chat_postMessage(channel=channel_id, text = 'Invalid value :(')
                    user_states.pop(user_id, None)
            else:
                try:
                    date = str(user_text.strip())
                    QUERY = '''SELECT COUNT(*) FROM houses
                    WHERE dates = %s;
                    '''
                    cursor.execute(QUERY, (date,))
                    result = cursor.fetchone()
                    result = list(result)[0]
                    client.chat_postMessage(channel=channel_id, text = f'There are {result} left.')
                    user_states.pop(user_id, None)
                except:
                    client.chat_postMessage(channel=channel_id, text = 'Invalid value :(')
                    user_states.pop(user_id, None)

        elif user_text == 'pr':
            user_states[user_id] = 'pr'
            client.chat_postMessage(channel=channel_id, text = 
                                '''Type the range or price u r looking for. (Example: 2000~4000)''')

        elif user_states.get(user_id) == 'pr':
            user_text = event.get('text')
            if '~' in user_text:
                range_parts = user_text.split('~')
                try:
                    num1 = int(range_parts[0].strip())
                    num2 = int(range_parts[1].strip())
                    QUERY = '''SELECT COUNT(*) FROM houses
                    WHERE price BETWEEN %s AND %s;
                    '''
                    cursor.execute(QUERY, (num1,num2,))
                    result = cursor.fetchone()
                    result = list(result)[0]
                    client.chat_postMessage(channel=channel_id, text = f'There are {result} left.')
                    user_states.pop(user_id, None)
                except :
                    client.chat_postMessage(channel=channel_id, text = 'Invalid value :(')
                    user_states.pop(user_id, None)
            else:
                try:
                    num = int(user_text.strip())
                    QUERY = '''SELECT COUNT(*) FROM houses
                    WHERE price = %s;
                    '''
                    cursor.execute(QUERY, (num,))
                    result = cursor.fetchone()
                    result = list(result)[0]
                    client.chat_postMessage(channel=channel_id, text = f'There are {result} left.')
                    user_states.pop(user_id, None)
                except:
                    client.chat_postMessage(channel=channel_id, text = 'Invalid value :(')
                    user_states.pop(user_id, None)

        elif user_text == 'ht':
            user_states[user_id] = 'ht'
            client.chat_postMessage(channel=channel_id, text = 'Which type? Example: 2bed|2bath')

        elif user_states.get(user_id) == 'ht':
            user_text = event.get('text')
            user_text.replace(' ','')
            user_text = user_text.lower()
            QUERY = '''SELECT count FROM ht_count
            WHERE house_type = %s;
            '''
            cursor.execute(QUERY, (user_text,))
            result = cursor.fetchone()
            result = list(result)[0]
            client.chat_postMessage(channel=channel_id, text = f'There are {result} left.')
            print(user_states.get(user_id))
            user_states.pop(user_id, None)
            print(user_states.get(user_id))


if __name__ == '__main__':
    app.run(debug=True)