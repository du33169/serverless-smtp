import os
from flask import Flask
from flask import request
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

secure = True if secure is not None and int(secure) == 1 else False
if port is None:
	port = 465
port=int(port)
smtp=SMTP(server=server,account=account,password=password,secure=secure,port=port)

app = Flask(__name__)
@app.route('/', methods=['GET','POST'])
def mail():
	if request.method == 'GET':
		return "Serverless SMTP Service is running, but you should use POST with json payload."
	
	elif request.method == 'POST':
		# get SenderName,to_addrs,subject,content from request in json
		sender_name = request.json.get('SenderName')
		to_addrs = request.json.get('to_addrs')
		subject = request.json.get('subject')
		content = request.json.get('content')

		# send email
		try:
			suc,msg=smtp.send_mail(sender_name,to_addrs,subject,content)
		except Exception as e:
			return f"error: {e}"
		return msg

if __name__ == '__main__':
	# not recommended for production use
	app.run(debug=True,host='0.0.0.0')