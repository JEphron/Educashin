from twilio.rest import TwilioRestClient


def send_text(reward, task):
    # Your Account Sid and Auth Token from twilio.com/user/account
    account_sid = "ACc3fd686eb31107436c4199b169bf6013"
    auth_token = "2791644d081d6aec6e813d49dc2d749f"
    client = TwilioRestClient(account_sid, auth_token)
    url = ""
    message = client.messages.create(body="Congratz! You earned %s for completing %s. Check out your money at %s" % (reward, task, url),
                                     to="+1 646-667-7202", from_="+1 646-542-0738")
    print message.sid
