
from pytz import timezone 
from datetime import datetime

import pytz
from settings import API_ID, API_HASH
from sys import argv, exit
from telethon import TelegramClient
from telethon.tl.types import UserStatusOnline, UserStatusOffline
from time import mktime, sleep

import telethon.sync


DATETIME_FORMAT = '%Y-%m-%d @ %H:%M:%S'
client = TelegramClient('tracker', API_ID, API_HASH)


def utc2localtime(utc):
    pivot = mktime(utc.timetuple())
    print(pivot)
    offset = datetime.fromtimestamp(pivot) - datetime.utcfromtimestamp(pivot)
    print(offset)
    return utc + offset



if len(argv) < 2:
    print(f'usage: {argv[0]} <contact id>')
    exit(1)
contact_id = argv[1]

client = TelegramClient('tracker', API_ID, API_HASH)
client.start()

online = None
last_offline = None
while True:
    if contact_id in ['me', 'self']:
        # Workaround for the regression in Telethon that breaks get_entity('me'):
        # https://github.com/LonamiWebs/Telethon/issues/1024
        contact = client.get_me()
    else:
        contact = client.get_entity(contact_id)

    if isinstance(contact.status, UserStatusOffline):
        if online != False:
            online = False
            ar = f'{utc2localtime(contact.status.was_online).strftime(DATETIME_FORMAT)} : User went offline.'
            print(ar + " " + contact_id)
            client.send_message('me', ar + ""+contact_id)
        elif last_offline != contact.status.was_online:
            if last_offline is not None:
                ar = f'{utc2localtime(contact.status.was_online).strftime(DATETIME_FORMAT)}: User went offline after being online for short time.'
                print(ar + " " + contact_id)
                client.send_message('me', ar + " " + contact_id)
            else:
                
                ar = f'{utc2localtime(contact.status.was_online).strftime(DATETIME_FORMAT)}: User went offline.'
                print(ar + " " + contact_id)
                client.send_message('me', ar + contact_id)
        last_offline = contact.status.was_online
    elif isinstance(contact.status, UserStatusOnline):
        if online != True:
            online = True
            ar = f'{datetime.now(timezone("Asia/Kolkata")).strftime(DATETIME_FORMAT)}: User went online.'
            print(ar + " " + contact_id)
            client.send_message('me', ar +" " + contact_id)
    else:
        if online != False:
            online = False
            ar = f'{datetime.now(timezone("Asia/Kolkata")).strftime(DATETIME_FORMAT)}: User went offline.'
            print(ar)
            client.send_message('me', ar + ""+contact_id) 
        last_offline = None
    sleep(15)

