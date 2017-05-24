from .iterators import iterable
import smtplib
from email.mime.text import MIMEText
from slacker import Slacker
import os


class Message(object):
    def __init__(self, recipient, body="", sender=None, subject=None, attachments=None):
        self.recipient = recipient
        self.sender = sender if sender is not None else recipient
        self.subject = subject
        self.body = body
        self.attachments = attachments


class NotificationService(object):
    def send(self, message=None, **kwargs):
        if message == None:
            return self.__send__(Message(**kwargs))
        if not isinstance(message, Message):
            raise RuntimeError("not an " + str(Message) + " instance")
        return self.__send__(message)


class EmailSendingService(NotificationService):
    def __init__(self, server_class=smtplib.SMTP,
                 additionnal_steps=None,
                 **server_args):
        self.server_class = server_class
        self.additionnal_steps = additionnal_steps
        self.server_args = server_args


    def __convert_to_MIMEText(self, message):
        m = MIMEText(message.body)
        m['From'] = message.sender
        m['To'] = message.recipient
        m['Subject'] = message.subject if message.subject is not None else "(empty)"
        return m


    def __send__(self, message):
        server = self.server_class(**self.server_args)
        server.ehlo()
        if callable(self.additionnal_steps):
            self.additionnal_steps(self)
        server.send_message(self.__convert_to_MIMEText(message))
        server.quit()


class SlackNotificationService(NotificationService):
    def __init__(self, slack_token):
        self.slack = Slacker(slack_token)


    def __slack_users(self):
        return self.slack.users.list().body['members']


    def __find_user_by_name(self, name):
        users = tuple(filter(lambda user: user["name"] == name, self.__slack_users()))
        if len(users) == 0:
            raise RuntimeError("no such user")
        if len(users) > 1:
            raise RuntimeError("inconsistent slack API, two users with same name")
        return users[0]["id"]

    def __format_message(self, message):
        if message.subject is None:
            return message.body
        else:
            return "*{}*\n{}".format(message.subject, message.body)

    def __send__(self, message):
        recipient = self.__find_user_by_name(message.recipient)
        channel = self.slack.im.open(recipient).body["channel"]["id"]
        self.slack.chat.post_message(channel, self.__format_message(message))
        if message.attachments is not None:
            if not iterable(message.attachments) or isinstance(message.attachments, str):
                attachments = (message.attachments,)
            else:
                attachments = message.attachments
            for attachment in attachments:
                self.slack.files.upload(channels=[channel],
                                        file_=attachment,
                                        filename=os.path.basename(attachment))
