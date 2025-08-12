import os
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

from app_flask import app
application = app

PORT = int(os.environ['LEANCLOUD_APP_PORT'])

if __name__ == '__main__':
	server = WSGIServer(('0.0.0.0', PORT), application, log=None, handler_class=WebSocketHandler)
	server.serve_forever()