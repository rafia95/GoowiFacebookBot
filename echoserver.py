from flask import Flask
from flask import request
import json
import requests

app = Flask(__name__)

# This needs to be filled with the Page Access Token that will be provided
# by the Facebook App that will be created.
PAT = 'EAAGFBcgLxk0BAJRwEv2snjQ5oyORqgpOZBBTPXy23LPbsT0vYjsEaAJw3BOHfSln1QEoawx8TjaIPgPhwmpI7FmM0cdGrCwmToJmhDXllCrHZCz164XmZC4bZB0M9zFYWN2gVkIsHidJ5f3CMn7R0mTs8kg82mD9b81cqAKrBAZDZD'
response = requests.post(
    "https://graph.facebook.com/v2.6/me/messenger_profile?access_token="+PAT,
    json={
        "get_started": {
            "payload": "GET_STARTED_PAYLOAD"
        }
    })

print "setting the start button" 
print response
@app.route('/', methods=['GET'])
def handle_verification():
  print "Handling Verification."
  if request.args.get('hub.verify_token', '') == 'my_voice_is_my_password_verify_me':
    print "Verification successful!"
    return 'Its good'
  else:
    print "Verification failed!"
    return 'Error, wrong validation token'

@app.route('/', methods=["POST"])
def handle_messages():
    payload = request.json

    print request.json
	print "in post"
    if 'entry' in payload:
        for entry in payload["entry"]:
            if "messaging" in entry:
                for message in entry["messaging"]:
                    print message
                    fbuid = message["sender"]["id"]
                    timestamp = datetime.fromtimestamp(int(message["timestamp"])/1000)

                    if "message" in message:
			print "Incoming from %s: %s" % (fbuid, message["message"]["text"])
   		        send_message(PAT, sender, 'this is the default reply')
                       
                    elif "postback" in message:
                        payload = message["postback"]["payload"]
			print payload
                        


    return "", 200



if __name__ == '__main__':
  app.run()