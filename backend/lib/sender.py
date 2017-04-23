# coding: utf-8

from django.conf import settings

from sendpulse_api import Client

from apps.sender.models import History


class External:
    def __init__(self, data):
        self.data = data
        self.send_pulse_conf = None
        self.send_pulse_key = None
        self.send_pulse_secret = None
        self.ff = None

        self.init_data()

    def init_data(self):
        self.send_pulse_conf = getattr(settings, 'SEND_PULSE')
        self.send_pulse_key = self.send_pulse_conf['id']
        self.send_pulse_secret = self.send_pulse_conf['secret']

        self.ff = {
            'html': self.data['html'],
            'text': self.data.get('text', ''),
            'subject': self.data['subject'],
            'from': {
                'name': self.send_pulse_conf['from']['name'],
                'email': self.send_pulse_conf['from']['email']
            },
            'to': [
                {'email': recipient} for recipient in self.data['to']
            ]
        }

    def recipients_to_str(self):
        return ', '.join([recipient['email'] for recipient in self.ff['to']])

    def send(self):
        history = History.objects.create(
            sender=self.ff['from']['email'],
            subject=self.ff['subject'],
            recipient=self.recipients_to_str()
        )

        client = Client(key=self.send_pulse_key, secret=self.send_pulse_secret)

        res = client.smtp_send_email(self.ff)

        if res.get('error_code'):
            history.comment = res['message']
        else:
            history.status = True

        history.save()

        return history.status