import os
import hmac
import hashlib
import time
import requests
from dotenv import load_dotenv

load_dotenv()

SLACK_SIGNING_SECRET = os.getenv('SLACK_SIGNING_SECRET')

# Verify Slack request signature
def verify_slack_request(request):
    timestamp = request.META.get('HTTP_X_SLACK_REQUEST_TIMESTAMP')
    if abs(time.time() - int(timestamp)) > 60 * 5:
        return False
    sig_basestring = f'v0:{timestamp}:{request.body.decode()}'
    my_signature = 'v0=' + hmac.new(
        SLACK_SIGNING_SECRET.encode(),
        sig_basestring.encode(),
        hashlib.sha256
    ).hexdigest()
    slack_signature = request.META.get('HTTP_X_SLACK_SIGNATURE')
    return hmac.compare_digest(my_signature, slack_signature)

# Send response to Slack
def send_slack_response(response_url, text):
    requests.post(response_url, json={"text": text})
