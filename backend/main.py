from threading import Timer
from flask import Flask, request, session, render_template, jsonify, redirect, url_for, send_from_directory
import rauth
import requests
from constants import *
import khan_api
import venmo_api
import twilio_sms
import pusher_api
from polling import poll_khan

app = Flask(__name__, static_url_path='/static')
app.debug = True
app.secret_key = VENMO_APP_SECRET
khan = khan_api.Khan()
venmo_oauth_url = 'https://api.venmo.com/v1/oauth/authorize?client_id=2844&scope=make_payments%20' \
                  'access_profile%20access_email%20access_phone%20access_balance&response_type=code'

# static
# @app.route('/img/<path:path>')
# def send_img(path):
#     return send_from_directory('img', path)
#
# @app.route('/fonts/<path:path>')
# def send_fonts(path):
#     return send_from_directory('fonts', path)
#
# @app.route('/css/<path:path>')
# def send_css(path):
#     return send_from_directory('css', path)
#
# @app.route('/js/<path:path>')
# def send_js(path):
#     return send_from_directory('js', path)

# catch all
# @app.before_request
def catch_all():
    print request.endpoint
    if 'venmo' not in session and request.endpoint != 'venmo_callback' and request.endpoint != 'index' and not 'static' in request.endpoint:
        return redirect(venmo_oauth_url)


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html', data={
        'sign_in': venmo_oauth_url
    })


@app.route('/venmo-callback')
def venmo_callback():
    AUTHORIZATION_CODE = request.args.get('code')
    data = {
        "client_id": VENMO_CONSUMER_ID,
        "client_secret": VENMO_CONSUMER_SECRET,
        "code": AUTHORIZATION_CODE
    }
    url = "%s/oauth/access_token" % (VENMO_API_URL,)
    response = requests.post(url, data)
    response_dict = response.json()
    access_token = response_dict.get('access_token')
    user = response_dict.get('user')
    session['venmo'] = {
        'oauth_token': access_token,
        'username': user['username'],
    }

    return redirect(url_for('parent_dashboard'))


@app.route('/parent/dashboard')
def parent_dashboard():
    if 'venmo' not in session:
        return redirect(venmo_oauth_url)

    data = {'name': session['venmo']['username'],
            'venmo_oauth': session.get('venmo', {}).get('oauth_token', ""),
            'khan_token': session.get('khan', {}).get('oauth_token', ""),
            'child_phone': session.get('child_phone', ''),
            'child_venmo': session.get('child_venmo', ''),
            'consumer_id': VENMO_CONSUMER_ID,
            'access_token': session['venmo']['oauth_token'],
            'signed_in': True}

    return render_template('dashboard.html', data=data)

@app.route('/child/dashboard')
def child_dashboard():
    if 'venmo' not in session:
        return redirect(venmo_oauth_url)

    data = {'name': session['venmo']['username'],
            'venmo_oauth': session.get('venmo', {}).get('oauth_token', ""),
            'khan_token': session.get('khan', {}).get('oauth_token', ""),
            'child_phone': session.get('child_phone', ''),
            'child_venmo': session.get('child_venmo', ''),
            'consumer_id': VENMO_CONSUMER_ID,
            'access_token': session['venmo']['oauth_token'],
            'signed_in': True}

    return render_template('child_dashboard.html', data=data)


@app.route('/poll-khan')
def poll_khan():
    token = session.get('khan', {}).get('oauth_token')


@app.route('/payout-trigger')
def payout_trigger():
    # do the venmo thing
    venmo_api.transfer(session['venmo']['oauth_token'], session['child_venmo'], 10.0, 'Completed Calculus 1')
    # send the text


@app.route('/link-khan')
def link_khan():
    authorize_url = khan.start_auth(url_for('khan_callback'))
    return redirect(authorize_url)  # takes you out of the site. Will return in khan_callback


@app.route('/khan-callback')
def khan_callback():
    session['khan'] = khan.finalize_auth(request)

    def cb(data, session_data):
        title = data['video']['translated_title']
        print title
        print "woot woot"
        twilio_sms.send_text('$10.00', title)
        pusher_api.push("You just finished watching %s" % (title,))
        venmo_api.transfer(session_data['venmo_oauth'], session_data['child_venmo_handle'], 10.00,
                           "Reward for watching %s" % (title,))

    khan.poll_changed_callback = cb

    def run_poll(khan, data):
        with app.test_request_context():
            res = khan.poll(data)
            Timer(2, run_poll, [khan, data]).start()

    run_poll(khan, {'ka_oauth': session['khan']['oauth_token'],
                    'venmo_oauth': session['venmo']['oauth_token'],
                    'child_venmo_handle': session['child_venmo']
                    })
    return redirect(url_for('parent_dashboard'))


@app.route('/link-child-venmo', methods=['POST'])
def link_child_venmo():
    session['child_venmo'] = request.form['venmo_id']
    session['child_phone'] = request.form['phone_num']
    return redirect(url_for('parent_dashboard'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
