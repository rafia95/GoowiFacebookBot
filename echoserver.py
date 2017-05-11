from flask import Flask
from flask import request
import json
import requests

app = Flask(__name__)


PAT = 'EAAGFBcgLxk0BAJRwEv2snjQ5oyORqgpOZBBTPXy23LPbsT0vYjsEaAJw3BOHfSln1QEoawx8TjaIPgPhwmpI7FmM0cdGrCwmToJmhDXllCrHZCz164XmZC4bZB0M9zFYWN2gVkIsHidJ5f3CMn7R0mTs8kg82mD9b81cqAKrBAZDZD'
quick_replies_list = [{
    "content_type":"text",
    "title":"Donate",
    "payload":"Donate",
}
]
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
                        "webview_height_ratio": "full",
                        "url": "https://dawson.goowi.com"
                    },
                    {
                        "type": "web_url",
                        "title": "I'd like to keep in touch",
                        "webview_height_ratio": "full",
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
  if request.args.get('hub.verify_token') == 'my_voice_is_my_password_verify_me':
    print "Verification successful!"
    return 'Its good'
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
                "text":"Goowi will contact you shortly with the answer.",
                "attachment":{
                            "type":"template",
                            "payload":{
                            "template_type":"generic",
                            "elements":[
                                       {
                                        "title":"Breaking News: Record Thunderstorms",
                                        "subtitle":"The local area is due for record thunderstorms over the weekend.",
                                        "image_url":"https://www.w3schools.com/css/img_fjords.jpg",
                                        "buttons":[
                                                  {
                                                   "type":"element_share"
                                                  }              
                                                  ]
                                      }
                                      ]
                                      }
                             }),
                               headers={'Content-type': 'application/json'})
    print r.text
    print "end"

if __name__ == '__main__':
  app.run()
