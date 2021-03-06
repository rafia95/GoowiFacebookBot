from flask import Flask
from flask import request
import json
import requests
import hashlib
import hmac
import base64

app = Flask(__name__)


PAT = 'EAAByUk5i2t4BADo8aEPw0poMt9czijMXzKTRt6KcYYNF2Kjb6j9IYS6vU1xgGbD7eZBLhFJnyRZBKsWnEc2PJsfDZCZCnA0uzMHfca2xIBaQBPaVq8eyEFKBewRKhS85sZB7UeTWjsnGnJ3M9hUv7CZB05JepP1CN8uG7PEpmIzwZDZD'

response = requests.post(
    "https://graph.facebook.com/v2.6/me/messenger_profile?access_token="+PAT,
    json={
          "setting_type":"call_to_actions",
          "thread_state":"new_thread",
          "call_to_actions": {
            "payload": "first hand shake"
        }
    })
response = requests.post(
    "https://graph.facebook.com/v2.6/me/messenger_profile?access_token="+PAT,
    json={
        "setting_type":"greeting",
        "greeting": [
            {
                "locale": "default",
                "text": "Goowi offers new ways to help make a change in the world by supporting charities. Please feel welcome to ask us questions."
            }
        ]
    })
response = requests.post(
    "https://graph.facebook.com/v2.6/me/messenger_profile?access_token="+PAT,
    json={
        "persistent_menu": [
            {
                "locale": "default",
                "composer_input_disabled": False,
                "call_to_actions": [
                    {
                        "type": "web_url",
                        "title": "I'd like to donate to dawson",
                        "webview_height_ratio": "compact",
                        "url": "https://dawson.goowi.com"
                    },
                    {
                        "type": "web_url",
                        "title": "I'd like to keep in touch",
                        "webview_height_ratio": "tall",
                        "url": "https://www.goowi.com"
                    }
                ]
            },
            {
                "locale": "zh_CN",
                "composer_input_disabled": False
            }
        ]
    })
@app.route('/', methods=['GET'])
def handle_verification():
  print "Handling Verification."
  print request.get_data()
  print request.args
  if "hub.verify_token" in request.values and "hub.mode" in request.values and "hub.challenge" in request.values:
        if request.values["hub.verify_token"] == 'my_voice_is_my_password_verify_me':
            print "Verification successful!"
            return request.values["hub.challenge"], 200
  return "bad token"


@app.route('/', methods=['POST'])
def handle_messages():
    print "Handling Messages"
    print request.args
    print request.headers
    print request.headers.get("X-Hub-Signature")
    signature = request.headers.get("X-Hub-Signature")
    payload = request.get_data()
    print payload
    hiddenkey = "3d39f740aa5d969e1a5bbb7b7dde643d"
    digester = hmac.new(hiddenkey,payload,hashlib.sha1)
    generated_signature = "sha1="+digester.hexdigest()
    print generated_signature
    if signature == generated_signature:
       print "Request is coming from facebook"
       for sender, message in messaging_events(payload):
           print "Incoming from %s: %s" % (sender, message)
           send_message(PAT, sender)
       return "ok"
    else: 
       print "Request not from facebook, signatures do not match!"
       return "Bad Request"

def messaging_events(payload):
    """Generate tuples of (sender_id, message_text) from the
    provided payload.
    """
    data = json.loads(payload)
    messaging_events = data["entry"][0]["messaging"]
    for event in messaging_events:
        if "message" in event and "text" in event["message"]:
            yield event["sender"]["id"], event["message"]["text"].encode('unicode_escape')
	elif "postback" in event and "payload" in event["postback"]:
            yield event["sender"]["id"], event["postback"]["payload"].encode('unicode_escape')
        else:
            yield event["sender"]["id"], "I can't echo this"


def send_message(token, recipient):
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", 
        params={
        "access_token": token},
        data=json.dumps({
                "recipient": {"id": recipient},
                "message":{
                "attachment":{
                              "type":"template",
                              "payload":{
                              "template_type":"generic",
                              "elements":[
                                         {
                                          "title":"Goowi will contact you shortly with the answer :).",
                                          "image_url":"https://www.goowi.com/faces/javax.faces.resource/images/logo.png",
                                          "buttons":[
                                                    {
                                                      "type":"element_share"
                                                    }              
                                                    ]
                                         }
                                         ]
                                        }
                             }
                           }
                       }),
                     headers={'Content-type': 'application/json'})
    print r.text
    print "end"

if __name__ == '__main__':
  app.run()
