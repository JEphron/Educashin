from datetime import datetime, timedelta
import json
import rauth
from constants import *
import dateutil.parser

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

    completed_items = []

    def poll(self, param):
        resource_url = DEFAULT_API_RESOURCE
        future = '2016-08-09T00:00:00Z'
        # print now.isoformat() + 'Z'
        start = datetime.utcnow() - timedelta(minutes=1)
        params = {'dt_start': start.isoformat() + 'Z', 'dt_end': future, 'username': 'JEphron63'}
        response = self.session.get(KHAN_SERVER_URL + resource_url, params=params)
        new_data = json.JSONDecoder().decode(response.text)
        # shared_items = set(new_data.items()) & set(self.data.items())
        # print len(shared_items)
        if len(new_data) is 0:
            return

        new_data.sort(key=lambda k: k['backup_timestamp'])

        current_entry = new_data[-1]
        # print current_entry
        print current_entry['completed'], current_entry['video']['relative_url']
        if current_entry['completed'] and not current_entry['video']['translated_youtube_id'] in self.completed_items:
            diff = datetime.utcnow() - dateutil.parser.parse(current_entry['backup_timestamp']).replace(tzinfo=None)
            print diff
            if diff < timedelta(seconds=30):
                self.completed_items.append(current_entry['video']['translated_youtube_id'])
                self.poll_changed_callback(new_data[-1])
