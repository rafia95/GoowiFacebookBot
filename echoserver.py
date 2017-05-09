from flask import Flask, request
import json
import requests

app = Flask(__name__)

# This needs to be filled with the Page Access Token that will be provided
# by the Facebook App that will be created.
PAT = 'EAAGFBcgLxk0BAJRwEv2snjQ5oyORqgpOZBBTPXy23LPbsT0vYjsEaAJw3BOHfSln1QEoawx8TjaIPgPhwmpI7FmM0cdGrCwmToJmhDXllCrHZCz164XmZC4bZB0M9zFYWN2gVkIsHidJ5f3CMn7R0mTs8kg82mD9b81cqAKrBAZDZD'

@app.route('/', methods=['GET'])
def handle_verification():
  print "Handling Verification."
  if request.values['hub.verify_token'] == 'my_voice_is_my_password_verify_me':
    print "Verification successful!"
    return request.values['hub.challenge'],200
  else:
    print "Verification failed!"
    return 'Error, wrong validation token'

@app.route('/', methods=['POST'])
def handle_messages():
  print "Handling Messages"
  payload = request.get_data()
  print payload
  for sender, message in messaging_events(payload):
    print "Incoming from %s: %s" % (sender, message)
    send_message(PAT, sender, 'this is the default reply')
  return "ok"

def messaging_events(payload):
  """Generate tuples of (sender_id, message_text) from the
  provided payload.
  """
  data = json.loads(payload)
  messaging_events = data["entry"][0]["messaging"]
  for event in messaging_events:
    if "message" in event and "text" in event["message"]:
      yield event["sender"]["id"], event["message"]["text"].encode('unicode_escape')
    else:
      yield event["sender"]["id"], "I can't echo this"


def send_message(token, recipient, text):
  """Send the message text to recipient with id recipient.
  """

  r = requests.post("https://graph.facebook.com/v2.6/me/messages",
    params={"access_token": token},
    data=json.dumps({
      "recipient": {"id": recipient},
      "message": {"text": text.decode('unicode_escape')}
    }),
    headers={'Content-type': 'application/json'})
  if r.status_code != requests.codes.ok:
    print r.text

if __name__ == '__main__':
  app.run()