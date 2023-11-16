from telethon import TelegramClient, events
from dotenv import load_dotenv
import os
import datetime
import json
import logging
import sys

logging.basicConfig(
    stream=sys.stdout,
    level=os.environ.get('LOGLEVEL', 'INFO').upper(),
    format='%(asctime)s [%(levelname)s] %(message)s',
)

load_dotenv()  # take environment variables from .env.

api_id = os.environ.get('TG_API_ID')
api_hash = os.environ.get('TG_API_HASH')
directory = os.environ.get('TG_DATA_DIR', '/tmp/tg_data')
channel_ids = os.environ.get('TG_CHANNELS', '').split(',')
channels = {}

if not os.path.exists(directory):
    logging.info('Creating directory %s', directory)
    os.makedirs(directory)

if not (api_id and api_hash):
    logging.error("Please set TG_API_ID, TG_API_HASH")
    exit(1)

client = TelegramClient(os.environ.get('TG_SESSION_ID', 'default'), api_id, api_hash)

async def init():

    me = await client.get_me()
    logging.info("Authenticated as %s", me.username or '-Anonymous-')

    async for dialog in client.iter_dialogs():
        if dialog.is_channel and dialog.entity.username in channel_ids:
            channels[dialog.entity.id] = dialog.entity
            logging.info("Listening to channel %s", dialog.entity.username)
    
    if len(channels.keys()) < 1:
        logging.error("Please set at least one channel in TG_CHANNELS")
        exit(1)

def main():
    with client:
        client.start()
        client.loop.run_until_complete(init())

        @client.on(events.NewMessage())
        async def handler(event):
            try:
                if not hasattr(event.message.peer_id, 'channel_id') or event.message.peer_id.channel_id not in channels.keys():
                    return

                channel = await client.get_entity(event.message.peer_id.channel_id)
                filename = os.path.join(directory, datetime.datetime.today().strftime("%Y-%m-%d") + ".ndjson")
                with open(filename, "a") as f:
                    logging.info("Reading message from %s at %s", channel.username, event.message.date.strftime("%Y-%m-%d %H:%M:%S"))
                    f.write(json.dumps({
                        "channel": channel.username,
                        "content": event.message.message,
                        "datetime": event.message.date.strftime("%Y-%m-%d %H:%M:%S")
                    }) + "\n")
            except Exception as e:
                logging.error("Exception occurred", e)
        try:
            client.run_until_disconnected()
        except ConnectionError: #catches the ConnectionError and starts the connections process again
            logging.error('Connection was closed. Reconnecting...')
            main()

if __name__ == "__main__":
    main()