"""

    @jesuisnuageux
    Create all settings for a good looking application

"""

import requests
import sys
PAT = 'EAAGFBcgLxk0BAJRwEv2snjQ5oyORqgpOZBBTPXy23LPbsT0vYjsEaAJw3BOHfSln1QEoawx8TjaIPgPhwmpI7FmM0cdGrCwmToJmhDXllCrHZCz164XmZC4bZB0M9zFYWN2gVkIsHidJ5f3CMn7R0mTs8kg82mD9b81cqAKrBAZDZD'
sys.stdout.write("> Cleaning previous settings ...")
sys.stdout.flush()
response = requests.delete(
    "https://graph.facebook.com/v2.6/me/messenger_profile?access_token="+PAT,
    json={
        "fields": [
            "persistent_menu",
            "get_started",
            "greeting",
        ]
    })
sys.stdout.write(" Got response : {} ({}) ... {}\n".format(response.reason, str(response.status_code), response.text))
sys.stdout.flush()

sys.stdout.write("> Setting up 'Getting Started' button ...")
sys.stdout.flush()
response = requests.post(
    "https://graph.facebook.com/v2.6/me/messenger_profile?access_token="+PAT,
    json={
        "get_started": {
            "payload": "GET_STARTED_PAYLOAD"
        }
    })
sys.stdout.write(" Got response : {} ({}) ... {}\n".format(response.reason, str(response.status_code), response.text))
sys.stdout.flush()

sys.stdout.write("> Setting up 'Greeting Message' button ...")
sys.stdout.flush()
response = requests.post(
    "https://graph.facebook.com/v2.6/me/messenger_profile?access_token={}".format(GOOWI_EVENTS_FACEBOOK_PAGE_TOKEN),
    json={
        "greeting": [
            {
                "locale": "default",
                "text": "Goowi offers new ways to help make a change in the world by supporting charities"
            }
        ]
    })
sys.stdout.write(" Got response : {} ({}) ... {}\n".format(response.reason, str(response.status_code), response.text))
sys.stdout.flush()

sys.stdout.write("> Setting up 'Call to actions' ...")
sys.stdout.flush()
response = requests.post(
    "https://graph.facebook.com/v2.6/me/messenger_profile?access_token="+PAT,
    json={
        "persistent_menu": [
            {
                "locale": "default",
                "composer_input_disabled": True,
                "call_to_actions": [
                    {
                        "type": "web_url",
                        "title": "I'd like to be a supporter",
                        "webview_height_ratio": "full",
                        "url": "https://blog.hartleybrody.com/fb-messenger-bot/"
                    },
                    {
                        "type": "web_url",
                        "title": "I'd like to keep in touch",
                        "webview_height_ratio": "full",
                        "url": "https://blog.hartleybrody.com/fb-messenger-bot/"
                    }
                ]
            },
            {
                "locale": "zh_CN",
                "composer_input_disabled": False
            }
        ]
    })
sys.stdout.write(" Got response : {} ({}) ... {}\n".format(response.reason, str(response.status_code), response.text))
sys.stdout.flush()

sys.stdout.write("> Getting current state ..."),
sys.stdout.flush()
response = requests.get(
    "https://graph.facebook.com/v2.6/me/messenger_profile",
    {
        "access_token": PAT,
        "fields": "persistent_menu,greeting,get_started"
    }
)
sys.stdout.write(" Got response : {} ({})\n".format(response.reason, str(response.status_code)))
sys.stdout.flush()
sys.stdout.write("\n")

data = response.json()["data"]
for row in data:
    for k in row.keys():
        print "{} -> {}".format(k, row[k])

print
