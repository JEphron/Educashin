import rauth
from constants import *


def start_auth(callback_url):
    service = rauth.OAuth1Service(
        name='test',
        consumer_key=KHAN_CONSUMER_KEY,
        consumer_secret=KHAN_CONSUMER_SECRET,
        request_token_url=KHAN_SERVER_URL + '/api/auth2/request_token',
        access_token_url=KHAN_SERVER_URL + '/api/auth2/access_token',
        authorize_url=KHAN_SERVER_URL + '/api/auth2/authorize',
        base_url=KHAN_SERVER_URL + '/api/auth2')

    cb_url = 'http://%s:%d%s' % (CALLBACK_BASE, 5000, callback_url)

    request_token, secret_request_token = service.get_request_token(
        params={'oauth_callback': cb_url})

    return service.get_authorize_url(request_token)

def finalize_auth(request):
    return {
        'oauth_token_secret': request.args.get('oauth_token_secret', ""),
        'oauth_verifier': request.args.get('oauth_verifier', ""),
        'oauth_token': request.args.get('oauth_token', "")
    }