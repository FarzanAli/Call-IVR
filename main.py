import requests
import os
from twilio.rest import Client
import time

# def createCall():
sid = os.environ["LIVE_SID"]
token = os.environ["LIVE_TOKEN"]
client = Client(sid, token)
call = client.calls.create(
    twiml='<Response><Start><Stream name="streaming" url="wss://8a65-2607-fea8-f4d9-4df0-b079-ce93-b72b-d0e2.ngrok-free.app/" /></Start><Dial>+18887643771</Dial></Response>',
    from_='+13656560656',
    to='+14163008698'
)

# newTwiml = '<Response><Gather timeout="10" numDigits="1"><Play digits="wwww1"/></Gather></Response>'
# time.sleep(20)
# client.calls(call.sid).update(twiml=newTwiml)
# print(call.sid)
# print(client.calls.list)


# while True:
#     call = client.calls(call.sid).fetch()
#     if call.status == 'in-progress':
#         break
#     time.sleep(1)

# print('first leg')

# # Monitor second leg of the call (the call that was dialed)
# while True:
#     dial_call = client.calls.list(parent_call_sid=call.sid)
#     if dial_call and dial_call[0].status == 'in-progress':
#         time.sleep(10)
#         # client.calls(call.sid).update(twiml=newTwiml)
#         break  # Exit loop if the dialed call is in-progress
#     time.sleep(1)  # Wait for 1 second before checking again

# print('second leg')
# time.sleep(10)
# print('after waiting')
# call = client.calls(call.sid).fetch()
# print(call)

# updated_call = client.calls(call.sid).update(twiml = newTwiml)

# print('Finished updating call')


# if __name__ == "__main__":
#     createCall()