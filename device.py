import sys, os, time 
#import fcntl,socket, struct
import json
import base64 
import paho.mqtt.client as mqtt
import paho.mqtt.publish
import utils
import hashlib
import hmac

reload(sys) 
sys.setdefaultencoding('utf-8')

broker = 'broker.hivemq.com'
topic = 'hanhet/simple-request'
compose_file = 'test.yml'
payload = ""
msg = ""
key = 'signature is unique'
hash_id= "" 

# If broker asks client id
client_id = ""
client = mqtt.Client(client_id=client_id)

# If broker asks user/password
user = ""
password = ""
client.username_pw_set(user, password)

# Generate service id
req_id = utils.getHwAddr('eth0')+utils.getAddress('adr')
print req_id
hash_id = hmac.new(key,req_id, hashlib.sha1)
signature = hash_id.hexdigest()
print signature
client.connect(broker, keepalive=60,bind_address="")

fp = open(compose_file, 'rb')
byte = fp.read()
fp.close()

# do bas64 encrption
msg = base64.b64encode(byte)
# print msg
data =  {"sid": signature, "req": msg}
payload = json.dumps(data)
# print "%s" % payload
client.publish(topic,"%s" % payload,qos=2,retain = True)
