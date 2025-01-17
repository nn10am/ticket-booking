from google.auth.transport import requests
from google.oauth2 import id_token
import requests as req
import os

def get_google_provider_cfg():
    return req.get(os.getenv("GOOGLE_DISCOVERY_URL")).json()

def get_user_info(token):
    try:
        id_info = id_token.verify_oauth2_token(token, requests.Request(), os.getenv("GOOGLE_CLIENT_ID"))
        return id_info
    except ValueError:
        return None
    