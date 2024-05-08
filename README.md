# LeanCloud SMTP Email Service

## Deploy
### Environment Variables

If you host the application on any cloud provider, there is somewhere in their dashboard to set these environment variables. Usually you are able to set some variables to be hidden, like `SMTP_PASSWORD`.

| env | desc | required? |
| ----- | ----- | -------|
|'SMTP_SERVER'| smtp host server address | yes |
|'SMTP_ACCOUNT'| smtp mail account  | yes |
|'SMTP_PASSWORD'| smtp password | yes |
|'SMTP_SECURE'| `1` or `0`, whether to enable SSL | optional |
|'SMTP_PORT'| smtp port, usually 465 for secure connection and 25 for insecure | optional |

### Deploy to LeanCloud

1. Create a Application in LeanCloud
2. Enter "Cloud Engine" Dashboard
3. Create a Group, for example, "default"
4. Enter Group Dashboard, Switch to "Setting" Tab
5. Add variables as described above and Save
6. Switch to "Deploy" Tab
7. Click "Git Deploy" Button
8. Click "Configure Git"
9. Copy and paste: `https://github.com/du33169/serverless-smtp.git`
10. "Save" and "Deploy"

### Local test/host

1. install requirements:
	```bash
	pip install -r requirements.txt
	```
2. Set environment variables as described before
3. start the application:
	```python
	python app.py
	```
	

**Note**: you may need to manually adjust the code in app.py to listen on the correct address and port.

## Usage

The application accept POST requests with json payload. Required fields:

| field        | desc                                                         |
| ------------ | ------------------------------------------------------------ |
| `SenderName` | Who send the mail. This should be a human-friendly name, not email address. |
| `to_addrs`   | a list containing who will receive this email                |
| `subject`    | title of the email                                           |
| `content`    | content of the email                                         |

An example to invoke the application using curl:

```bash
curl -X POST http://address:port -H "Content-Type: application/json" -d '{	"SenderName": "John Doe","to_addrs": ["you@example.com"],	"subject": "Title",	"content": "Hello World!"}'
```