from datetime import datetime, timedelta
import json
import rauth
from constants import *

DEFAULT_API_RESOURCE = '/api/v1/user/videos'


class Khan():
    service = None
    session = None
    request_token = secret_request_token = None
    data = None
    poll_changed_callback = None

    def start_auth(self, callback_url):
        self.service = rauth.OAuth1Service(
            name='test',
            consumer_key=KHAN_CONSUMER_KEY,
            consumer_secret=KHAN_CONSUMER_SECRET,
            request_token_url=KHAN_SERVER_URL + '/api/auth2/request_token',
            access_token_url=KHAN_SERVER_URL + '/api/auth2/access_token',
            authorize_url=KHAN_SERVER_URL + '/api/auth2/authorize',
            base_url=KHAN_SERVER_URL + '/api/auth2')

        cb_url = 'http://%s:%d%s' % (CALLBACK_BASE, 5000, callback_url)

        self.request_token, self.secret_request_token = self.service.get_request_token(
            params={'oauth_callback': cb_url})

        return self.service.get_authorize_url(self.request_token)

    def finalize_auth(self, request):
        self.session = self.service.get_auth_session(self.request_token, self.secret_request_token,
                                                     params={'oauth_verifier': request.args.get('oauth_verifier', "")})

        return {
            'oauth_token_secret': request.args.get('oauth_token_secret', ""),
            'oauth_verifier': request.args.get('oauth_verifier', ""),
            'oauth_token': request.args.get('oauth_token', "")
        }

    def poll(self, param):
        resource_url = DEFAULT_API_RESOURCE
        now = datetime.now()
        print now.isoformat() + 'Z'
        prev = '2011-08-08T22:46:24Z'
        params = {'dt_start': prev, 'dt_end': now.isoformat() + 'Z', 'username': 'JEphron63'}
        response = self.session.get(KHAN_SERVER_URL + resource_url, params=params)
        new_data = json.JSONDecoder().decode(response.text)
        shared_items = set(new_data.items()) & set(self.data.items())
        print len(shared_items)
        if len(new_data) > len(self.data):
            self.poll_changed_callback()
            self.data = new_data
        return self.data
