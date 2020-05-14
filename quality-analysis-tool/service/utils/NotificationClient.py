from service.utils.RestClient import RestClient
import json


class NotificationClient:

    def __init__(self, url, url_param, channel, user_name):
        self.url = url
        self.url_param = url_param
        self.headers = {'accept': 'application/json', 'Content-Type': 'application/json'''}
        self.channel = channel
        self.user_name = user_name

    def post_notification(self, payload):

        body = {"channel": self.channel, "username": self.user_name, "text": payload, "icon_emoji": ":mega:"}

        rest_client = RestClient(self.url, self.url_param)

        result = rest_client.post_to_webhook(body, self.headers)

        return result

