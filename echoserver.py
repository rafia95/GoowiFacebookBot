from flask import Flask
from flask import request
import json
import requests

app = Flask(__name__)


PAT = 'EAAac8i8oLpQBAHoF5d0wQ6zOTtmpCvv6H9anamdGLip8A4iOD5eapr3wVZBekblcGyZCJEviIdc2JUucH8Eu83Vkdo6yAiQx7OZAtgz7axo27pt8e3YaS3fRXuXK0DNhWHRRlzmq2NBGBEOZAJ3336ZAlGl8aamT2euEjrWGSlwZDZD'

response = requests.post(
    "https://graph.facebook.com/v2.6/me/messenger_profile?access_token="+PAT,
    json={
          "setting_type":"call_to_actions",
          "thread_state":"new_thread",
          "get_started": {
            "payload": "First hand shake"
          }
         })
print "get stared send , sending menu"
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
                        "title": "I'd like to donate",
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
  print request.args
  if request.args.get('hub.verify_token', '') == 'my_voice_is_my_password_verify_me':
    print "Verification successful!"
    return request.args.get('hub.challenge', '')
  else:
    print "Verification failed :(!"
    return 'Error, wrong validation token :(('

@app.route('/', methods=['POST'])
def handle_messages():
    print "Handling Messages"
    payload = request.get_data()
    print payload
    for sender, message in messaging_events(payload):
        print "Incoming from %s: %s" % (sender, message)
        send_message(PAT, sender)
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
