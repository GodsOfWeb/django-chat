from django.shortcuts import render_to_response
from chat.models import Room, Message
import simplejson as json
import time
import gevent.select
import redis
import uwsgi

def home(request):
    try:
        room = Room.objects.get(pk=1)
    except:
        room = None
    return render_to_response('home.html', {'room':room})

def chat(request):
    try:
        room = Room.objects.get(pk=1)
    except:
        room = None

    uwsgi.websocket_handshake(request['HTTP_SEC_WEBSOCKET_KEY'], request.get('HTTP_ORIGIN', ''))
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    channel = r.pubsub()
    channel.subscribe(room.name)
    websocket_fd = uwsgi.connection_fd()
    redis_fd = channel.connection._sock.fileno()
    while True:
        ready = gevent.select.select([websocket_fd, redis_fd], [], [], 4.0)
        if not ready[0]:
            uwsgi.websocket_recv_nb()
        for fd in ready[0]:
            if fd == websocket_fd:
                msg = uwsgi.websocket_recv_nb()
                if msg:
                    msg = json.loads(msg)
                    if msg['c'] == 'm':
                        first_msg = "%s: %s" % (msg['u'], msg['ms'])
                        second_msg = None
                        if first_msg and not second_msg:
                            r.publish(room.name, first_msg)
                        elif second_msg and first_msg:
                            r.publish(room.name, "%s <br> %s" % (first_msg, second_msg))
            elif fd == redis_fd:
                msg = channel.parse_response() 
                if msg[0] == 'message':
                    uwsgi.websocket_send("[%s] %s" % (time.time(), msg[2]))
