import sys, os, time 
#import fcntl,socket, struct
import json
import base64 
import paho.mqtt.client as mqtt
import utils

reload(sys) 
sys.setdefaultencoding('utf-8')

broker = 'iot.eclipse.org'
topic = 'hanhet/simple-request'
compose_file = 'test.yml'
payload = ""
msg = ""
qos = 2

# If broker asks client id
client_id = ""
client = mqtt.Client(client_id=client_id)

# If broker asks user/password
user = ""
password = ""
client.username_pw_set(user, password)

# Generate service id
req_id = utils.getHwAddr('eth0')

client.connect(broker)

fp = open(compose_file, 'rb')
byte = fp.read()
fp.close()

# do bas64 encrption
msg = base64.b64encode(byte)
# print msg
data =  {"sid": req_id, "req": msg}
payload = json.dumps(data)
# print "%s" % payload
client.publish(topic, "%s" % payload)
