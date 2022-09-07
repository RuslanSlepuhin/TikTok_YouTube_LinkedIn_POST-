import json
import os
import time
from random import randrange

from flask import Flask
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import flask

'''
!!!! Usefull links !!!!! 
https://github.com/googleapis/google-api-python-client
https://developers.google.com/docs/api/quickstart/python

https://github.com/youtube/api-samples
https://developers.google.com/youtube/v3/docs
https://developers.google.com/youtube/v3/determine_quota_cost
'''

API_KEY = 'AIzaSyBT4pFKcqG0WZU8yHJOOZDYXz9V68LRl4s'
APP_TOKEN_FILE = "client_secret.json"
USER_TOKEN_FILE = "user_token.json"

# https://developers.google.com/identity/protocols/oauth2/scopes#youtube
SCOPES = [
    'https://www.googleapis.com/auth/youtube.force-ssl',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/youtube.upload',
    # 'https://www.googleapis.com/auth/userinfo.email'
]

server = Flask(__name__)

'''
Ask from console
'''
def get_creds_cons():
    flow = InstalledAppFlow.from_client_secrets_file(APP_TOKEN_FILE, SCOPES)
    return flow.run_console()


'''
Reusebale user OAuth2 token
'''
def get_creds_saved():
    # https://developers.google.com/docs/api/quickstart/python
    creds = None

    if os.path.exists(USER_TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(USER_TOKEN_FILE, SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(APP_TOKEN_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(USER_TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    return creds


# '''
# Get YouTube API service w API Key only
# '''
# def get_service():
#     # creds = get_creds_cons()
#     creds = get_creds_saved()
#     service = build('oauth2', 'v2', credentials=creds)
#     return service


def get_service_creds(service = 'youtube', version = 'v3'):
    creds = get_creds_saved()
    service = build(service, version, credentials=creds)
    return service

#
# '''
# Get User Info
# '''
# def get_user_info(channel_id='UCf6kozNejHoQuFhBDB8cfxA'):
#     r = get_service().userinfo().get().execute()
#     print(json.dumps(r))

@server.route('/')
def description():
    return 'For upload video to youtube you must go /upload'

@server.route('/upload')
def video_upload(video_path='video_text_done.mp4', title='TikTok', **kwargs):
    print("** upload video")

    # chunksize размер блока в БАЙТАХ (int), чем хуже соединение, тем мельче блок
    # напр. для мобильного трафа норм 1024*1024*3 = 3М
    # -1 => видос будет грузиться целиком, быстрее на норм сети и при обрыве все равно будет докачка
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)

    # список полей см здесь https://developers.google.com/youtube/v3/docs/videos/insert
    meta = {
        'snippet': {
            'title' : title,
            'description' : kwargs.get("description", "empty desc")
        },
        # All videos uploaded via the videos.insert endpoint from unverified API projects created after 28 July 2020
        # will be restricted to private viewing mode. To lift this restriction,
        # each API project must undergo an audit to verify compliance
        # --- т.е. для прилки в статусе теста тут всегда приват, иначе видос будет заблокирован
        'status':{
            'privacyStatus':kwargs.get("privacy", "private")
        }
    }

    insert_request = get_service_creds("youtube", "v3").videos().insert(
        part=','.join(meta.keys()),
        body=meta,
        media_body=media
    )

    r = resumable_upload(insert_request)

    print(r)

    return r


def resumable_upload(request, retries = 5):
    while retries > 0:
        try:
            status, response = request.next_chunk()
            if response is None: continue # next chunk, will be None until the resumable media is fully uploaded
            if 'id' not in response: raise Exception("no id found while video uploading")

            return response # success
        except Exception as e:
            print(e)
            retries -= 1
            time.sleep(randrange(5))

    return None



if __name__ == '__main__':
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
    video_upload(video_path='video_text_done.mp4', title='TikTok')
