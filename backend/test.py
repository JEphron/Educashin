""" An interactive script for testing Khan Academy API Authentication. 

This is an example of how to use the /api/auth2 authentication flow.

See https://github.com/Khan/khan-api/wiki/Khan-Academy-API-Authentication for
documentation.
"""
from datetime import datetime, date, time,timedelta
import cgi
import rauth
import SimpleHTTPServer
import SocketServer
# import time
import urllib
import webbrowser

# You can get a CONSUMER_KEY and CONSUMER_SECRET for your app here:
# http://www.khanacademy.org/api-apps/register
# CONSUMER_KEY = ''
# CONSUMER_SECRET = ''
session = None
CALLBACK_BASE = '127.0.0.1'
SERVER_URL = 'http://www.khanacademy.org'

DEFAULT_API_RESOURCE = '/api/v1/user/exercises/progress_changes'
VERIFIER = None


# Create the callback server that's used to set the oauth verifier after the
# request token is authorized.
def create_callback_server():
    class CallbackHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
        def do_GET(self):
            global VERIFIER

            params = cgi.parse_qs(self.path.split('?', 1)[1],
                keep_blank_values=False)
            VERIFIER = params['oauth_verifier'][0]

            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write('OAuth request token fetched and authorized;' +
                ' you can close this window.')

        def log_request(self, code='-', size='-'):
            pass

    server = SocketServer.TCPServer((CALLBACK_BASE, 0), CallbackHandler)
    return server


# Make an authenticated API call using the given rauth session.
def get_api_resource(session):
    SERVER_URL = 'http://www.khanacademy.org'

    DEFAULT_API_RESOURCE = '/api/v1/user/exercises/progress_changes'
    resource_url = DEFAULT_API_RESOURCE

    # start = time.time()
    now = datetime.now() 
    prev = datetime.now() - timedelta(seconds=3)
    # print prev.isoformat()
    params = {'dt_start':prev.isoformat()+'Z', 'dt_end':now.isoformat()+'Z'}
    # url = urllib.urlencode()
    # print url
    # print url
    response = session.get(SERVER_URL + resource_url,params = params)
    # end = time.time()

    # print "\n"
    return response.text
    # print "\nTime: %ss\n" % (end - start)


def getData(CONSUMER_KEY, CONSUMER_SECRET):
    global session
    # global CONSUMER_KEY, CONSUMER_SECRET, SERVER_URL
    
    # Set consumer key, consumer secret, and server base URL from user input or
    # use default values.
    # CONSUMER_KEY = raw_input("consumer key: ") or CONSUMER_KEY
    # CONSUMER_SECRET = raw_input("consumer secret: ") or CONSUMER_SECRET
    # SERVER_URL = raw_input("server base url: ") or SERVER_URL

    # Create an OAuth1Service using rauth.
    if session is None:
        service = rauth.OAuth1Service(
               name='test',
               consumer_key=CONSUMER_KEY,
               consumer_secret=CONSUMER_SECRET,
               request_token_url=SERVER_URL + '/api/auth2/request_token',
               access_token_url=SERVER_URL + '/api/auth2/access_token',
               authorize_url=SERVER_URL + '/api/auth2/authorize',
               base_url=SERVER_URL + '/api/auth2')

        callback_server = create_callback_server()

        # 1. Get a request token.
        request_token, secret_request_token = service.get_request_token(
            params={'oauth_callback': 'http://%s:%d/' %
                (CALLBACK_BASE, callback_server.server_address[1])})
        
        # 2. Authorize your request token.
        authorize_url = service.get_authorize_url(request_token)
        webbrowser.open(authorize_url)

        callback_server.handle_request()
        callback_server.server_close()

        # 3. Get an access token.
        session = service.get_auth_session(request_token, secret_request_token,
            params={'oauth_verifier': VERIFIER})

    # Repeatedly prompt user for a resource and make authenticated API calls.
    return get_api_resource(session)
