from constants import *
import requests

def transfer(sender_token, receiver_email, amount, note):
    data = {
        "client_id": VENMO_CONSUMER_ID,
        "client_secret": VENMO_APP_SECRET,
        "access_token": sender_token,
        "email": receiver_email,
        "note": note,
        'amount': amount
    }
    url = "%s/payments" % (VENMO_API_URL,)
    response = requests.post(url, data)
    return response