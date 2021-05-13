from twilio.rest import Client

account_sid = 'AC079c58693b2f2b23330d76a774f40000'
auth_token = '0690d01528f8844283784625d34214a3'
    
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                    body="Hello",
                    from_='+18183505192',
                    to='+917807445246'

                )
print(message.status)
print(message.sid)