DJANGO-CHAT
===


Django-chat app using Websockets, uWSGI, Gevent and Redis

## Application setup:

    def application(env, start_response):
        if settings.MULTI_DOMAIN:
            host = env['HTTP_HOST']
            path = env['PATH_INFO']
            if _is_valid_path("/"+slugify(host) + path):
                env['PATH_INFO'] = "/" +slugify(host) + path
            elif _is_valid_path("/"+slugify(host) + path + "/"):
                env['PATH_INFO'] = "/" +slugify(host) + path + "/"
        if env['PATH_INFO'] == '/chat/':
            from chat.views import chat
            chat(env)
        else:
            return djangoapp(env,start_response)

## uWSGI settings:

    offload-threads = 2
    gevent = 100
    gevent-monkey-patch = True
    http-raw-body = True

## Javascript

    var SOCKET_ADDRESS = "ws://127.0.0.1:8080/chat/";

    $(document).ready(function(){
        ws = new WebSocket(SOCKET_ADDRESS);

        //Sends something trought websocket
        $("#send").click(function() {
            ws.send('{"c":"m", "ms":"'+$("#testo").val()+'", "u":"'+$("#nickname").val()+'"}');
        });

        //Receive something trought websocket
        ws.onmessage = function(e) {
            $("#blackboard").append("<p>"+e.data+"</p>");
        };

        ws.onerror = function(e) {
                console.log(e);
        };
    });
