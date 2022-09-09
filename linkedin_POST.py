import ast
import configparser
import requests

config = configparser.ConfigParser()
config.read("config.ini")

client_id = config['LinkedIn']['client_id']
client_secret = config['LinkedIn']['client_secret']
access_token = config['LinkedIn']['access_token']

url_information = 'https://api.linkedin.com/v2/me'
url_post = 'https://api.linkedin.com/v2/ugcPosts'

headers = {
    "Authorization": f"Bearer {access_token}",
}

#-------------------get information about me ------------------
response = requests.get(url_information, headers=headers)
id_user = ast.literal_eval(response.content.decode('utf-8'))['id']

#-------------------post to LinkedIn TEXT------------------
data = {
    "author": f"urn:li:person:{id_user}",
    "lifecycleState": "PUBLISHED",
    "specificContent": {
        "com.linkedin.ugc.ShareContent": {
            "shareCommentary": {
                "text": "Testing LinkedIn API"
            },
            "shareMediaCategory": "NONE"
        }
    },
    "visibility": {
        "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
    }
}

response = requests.post(url_post, json=data, headers=headers)
print(response.content)
