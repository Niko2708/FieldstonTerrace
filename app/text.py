import os
from twilio.rest import Client

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'AC1b7edfb714679a6f713f4d7a3eb2032e'
auth_token = 'f79a17f72094906431f081203e6b8a83'
client = Client(account_sid, auth_token)

def send_maintenance_text(users, post):
    for user in users:
        if user.text_notification:
            message = client.messages \
                .create(
                body=post.body,
                from_='+12182768257 ',
                to= user.phone_number
            )

            print(message.sid)