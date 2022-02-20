from twilio.rest import Client 
 
account_sid = 'AC9b188e7a13fe11e12178dbd34b931196' 
auth_token = 'c6e39a03d52523b84ecb3c4a92d8e2d3' 
client = Client(account_sid, auth_token) 
 
message = client.messages.create( 
                              from_='whatsapp:+14155238886',  
                              body='this an automated message using python and twilio from sayed',      
                              to='whatsapp:+201096686179' 
                          ) 
 
print(message.sid)




# import pywhatkit

# pywhatkit.sendwhatmsg('+2001009606610', 'Hello From Python')