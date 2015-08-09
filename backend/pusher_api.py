import pusher

def push(msg):
    p = pusher.Pusher(
      app_id='134359',
      key='c9da65d5b2527ee603e9',
      secret='21dcb43dbc0987c39a0f',
      ssl=True,
      port=443
    )
    p.trigger('test_channel', 'my_event', {'message': msg})
