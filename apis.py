import http.client
import json
import os
from dotenv import load_dotenv

load_dotenv()

PANTRY_ID = os.getenv('PANTRY_ID')
BLOCKCHAIN_BASKET_NAME = os.getenv('BLOCKCHAIN_BASKET_NAME')
KEY_BASKET_NAME = os.getenv('KEY_BASKET_NAME')
LOGGER_BASKET_NAME = os.getenv('LOGGER_BASKET_NAME')
conn = http.client.HTTPSConnection("getpantry.cloud")
headers = {
    'Content-Type': 'application/json'
}
null_payload = ''


def get_api_keys():
    try:
        conn.request("GET", "/apiv1/pantry/" + PANTRY_ID + "/basket/" + KEY_BASKET_NAME, null_payload, headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data.decode("utf-8"))
        master_keys = data
        return data
    except Exception as e:
        print(e)


def update_api_keys(updated_keys):
    try:
        payload = json.dumps(updated_keys)
        conn.request("POST", "/apiv1/pantry/" + PANTRY_ID + "/basket/" + KEY_BASKET_NAME, payload, headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data.decode("utf-8"))
        return data
    except Exception as e:
        print(e)


def update_blockchain(updated_data):
    try:
        payload = json.dumps(updated_data)
        conn.request("POST", "/apiv1/pantry/" + PANTRY_ID + "/basket/" + BLOCKCHAIN_BASKET_NAME, payload, headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data.decode("utf-8"))
        return data
    except Exception as e:
        print(e)


def get_blockchain():
    try:
        conn.request("GET", "/apiv1/pantry/" + PANTRY_ID + "/basket/" + BLOCKCHAIN_BASKET_NAME, null_payload, headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data.decode("utf-8"))
        return data
    except Exception as e:
        print(e)


def get_log_files():
    try:
        conn.request("GET", "/apiv1/pantry/" + PANTRY_ID + "/basket/" + LOGGER_BASKET_NAME, null_payload, headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data.decode("utf-8"))
        return data
    except Exception as e:
        print(e)


def push_log(log):
    try:
        payload = json.dumps({"LOG:": log})
        conn.request("PUT", "/apiv1/pantry/" + PANTRY_ID + "/basket/" + LOGGER_BASKET_NAME, payload, headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data.decode("utf-8"))
        return data
    except Exception as e:
        print(e)
