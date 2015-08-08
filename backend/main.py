from flask import Flask, request, session, render_template, jsonify, redirect, url_for
import rauth
import requests
from constants import *
import threading
"""
This file contains all the functions and routes for our demo app.
"""
app = Flask(__name__)
# comment out when you're done testing
app.debug = True
app.secret_key = VENMO_APP_SECRET  # a secret string that will sign your session cookies

# catch all
@app.before_request
def catch_all():
    if 'venmo' not in session:
        return redirect(url_for('index'))

@app.route('/')
@app.route('/index.html')
def index():
    url = 'https://api.venmo.com/v1/oauth/authorize?client_id=2844&scope=make_payments%20access_profile%20access_email%20access_phone%20access_balance&response_type=code'
    return redirect(url)


@app.route('/venmo-callback')
def oauth_authorized():
    AUTHORIZATION_CODE = request.args.get('code')
    data = {
        "client_id": VENMO_CONSUMER_ID,
        "client_secret": VENMO_CONSUMER_SECRET,
        "code": AUTHORIZATION_CODE
    }
    url = "https://api.venmo.com/v1/oauth/access_token"
    response = requests.post(url, data)
    response_dict = response.json()
    access_token = response_dict.get('access_token')
    user = response_dict.get('user')
    session['venmo'] = {
        'oauth_token': access_token,
        'username': user['username'],
    }

    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    print session.get('child_venmo', '')
    data = {'name': session['venmo']['username'],
            'khan_token': session.get('khan', {}).get('oauth_token', ""),
            'child_phone': session.get('child_phone', ''),
            'child_venmo': session.get('child_venmo', ''),
            'consumer_id': VENMO_CONSUMER_ID,
            'access_token': session['venmo']['oauth_token'],
            'signed_in': True}

    return render_template('dashboard.html', data=data)


@app.route('/poll-khan')
def poll_khan():
    token = session.get('khan', {}).get('oauth_token')


@app.route('/link-khan')
def link_khan():
    service = rauth.OAuth1Service(
        name='test',
        consumer_key=KHAN_CONSUMER_KEY,
        consumer_secret=KHAN_CONSUMER_SECRET,
        request_token_url=KHAN_SERVER_URL + '/api/auth2/request_token',
        access_token_url=KHAN_SERVER_URL + '/api/auth2/access_token',
        authorize_url=KHAN_SERVER_URL + '/api/auth2/authorize',
        base_url=KHAN_SERVER_URL + '/api/auth2')

    cb_url = 'http://%s:%d%s' % (CALLBACK_BASE, 5000, url_for('khan_callback'))
    print cb_url

    request_token, secret_request_token = service.get_request_token(
        params={'oauth_callback': cb_url})
    print session['venmo']
    authorize_url = service.get_authorize_url(request_token)

    # spawn off a polling thread
    def poll():
        threading.Timer(2, poll).start()
    return redirect(authorize_url)


@app.route('/khan-callback')
def khan_callback():
    print session['venmo']
    session['khan'] = {
        'oauth_token_secret': request.args.get('oauth_token_secret'),
        'oauth_verifier': request.args.get('oauth_verifier'),
        'oauth_token': request.args.get('oauth_token')
    }
    return redirect(url_for('dashboard'))


@app.route('/link-child-venmo', methods=['POST'])
def link_child_venmo():
    session['child_venmo'] = request.form['venmo_id']
    session['child_phone'] = request.form['phone_num']
    return redirect(url_for('dashboard'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
