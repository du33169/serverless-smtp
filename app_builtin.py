import os
from SMTP import SMTP

# get server,account,password from environment variables, save to variables
server = os.environ.get('SMTP_SERVER')
account = os.environ.get('SMTP_ACCOUNT')
password = os.environ.get('SMTP_PASSWORD')
secure = os.environ.get('SMTP_SECURE')
port = os.environ.get('SMTP_PORT')

assert server is not None, "SMTP_SERVER is not set"
assert account is not None, "SMTP_ACCOUNT is not set"
assert password is not None, "SMTP_PASSWORD is not set"

secure = True if secure is None or int(secure) == 1 else False
print(f"Secure Conection: {secure}")
if port is None:
	port = 465
port=int(port)
smtp=SMTP(server=server,account=account,password=password,secure=secure,port=port)

from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class RequestHandler(BaseHTTPRequestHandler):
	def _set_response(self, status_code=200, content_type="application/json;charset=UTF-8"):
		self.send_response(status_code)
		self.send_header('Content-type', content_type)
		self.end_headers()

	def do_GET(self):
		self._set_response()
		msg="Serverless SMTP Service is running, but you should use POST with json payload."
		# self.wfile.write(.encode('utf-8'))
		# return such body: 
		res={"statusCode": 200, "isBase64Encoded": False, "headers": {"Content-Type": "application/json;charset=UTF-8"},"body":msg}
		self.wfile.write(json.dumps(res).encode('utf-8'))

	def do_POST(self):
		content_length = int(self.headers['Content-Length'])
		post_data = self.rfile.read(content_length).decode('utf-8')
		json_data = json.loads(post_data)

		# get SenderName,to_addrs,subject,content from request in json
		sender_name = json_data.get('SenderName')
		to_addrs    = json_data.get('to_addrs')
		subject     = json_data.get('subject')
		content     = json_data.get('content')

		# send email
		try:
			suc,msg=smtp.send_mail(sender_name,to_addrs,subject,content)
		except Exception as e:
			msg=f"error: {e}"

		self._set_response()
		res={"statusCode": 200, "isBase64Encoded": False, "headers": {"Content-Type": "application/json;charset=UTF-8"},"body":msg}
		self.wfile.write(json.dumps(res).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=RequestHandler, addr="0.0.0.0", port=8000):
	server_address = (addr, port)
	httpd = server_class(server_address, handler_class)
	print(f'Starting http server on {addr}:{port}')
	httpd.serve_forever()

if __name__ == '__main__':
	run()
