import time
from threading import Timer

def poll_khan(callback):
    ret = get_data('BwjZZ2M9QvN7AyN3','Fbn8AHy4XBAAaDbp').strip(']').strip('[')
    # if 0 == len(ret):
    t = Timer(1, poll_khan, [callback])
    t.start()

    print ret

    # else:
    #     callback(ret)
    #     t = Timer(1, poll_khan, [callback])
    #     t.start()


def get_data(CONSUMER_KEY, CONSUMER_SECRET):
    return get_api_resource(session)


# Make an authenticated API call using the given rauth session.
def get_api_resource(session):
    SERVER_URL = 'http://www.khanacademy.org'

    # DEFAULT_API_RESOURCE = '/api/v1/user/exercises/progress_changes'
    resource_url = DEFAULT_API_RESOURCE

    # start = time.time()
    now = datetime.now()
    print now.isoformat()+'Z'
    prev = datetime.now() - timedelta(seconds=3)
    # print prev.isoformat()
    params = {'dt_start':prev.isoformat()+'Z', 'dt_end':now.isoformat()+'Z'}
    # url = urllib.urlencode()
    # print url
    # print url
    response = session.get(SERVER_URL + resource_url, params = params)
    cached_json = response
    # end = time.time()

    # print "\n"
    print response
    return response.text
    # print "\nTime: %ss\n" % (end - start)


