import atexit
import sys, os, time
import json
import paho.mqtt.client as mqtt
import utils
import hashlib
import hmac

reload(sys)
sys.setdefaultencoding('utf-8')
client = None
broker = "broker.hivemq.com"
prefix = 'ucan_coo'
topic = prefix+'/search/request'
payload=""
msg=""
key = 'signature is unique'
hash_id = ""
client_id=""
client = mqtt.Client(client_id=client_id)
username = ""
password = ""
count=0
client.username_pw_set(username, password)
#def mqtt_device_pub_search():
req_id = utils.getHwAddr()+utils.getAddress('adr')
hash_id = hmac.new(key,req_id, hashlib.sha1)
signature = hash_id.hexdigest()
mem = input("How much mem do you  needs at least?")
disk = input("How mush disk do you needs at least?")
print type(mem)
print type(disk)
requestdata = {"client_id":signature,"memory":{"totalmem":str(mem),"remainmem":str(mem)},"disk":{"totaldisk":str(disk),"remaindisk":str(disk)}}
payload=json.dumps(requestdata)
topic2 = prefix+'/search/response/'+signature 
print topic2
def on_connect(mq, userdata, flag, rc):
   print rc
   mq.publish(topic,payload,qos=2)
   mq.subscribe(topic2, qos=2)
def on_message(mq, userdata, msg):
   print msg.topic
   print msg.payload
def mqtt_device_sub():
   global client,mqtt_looping
   client = mqtt.Client(client_id=client_id)
   #client.username_pw_set(username,password)
   client.on_connect = on_connect
   client.on_message = on_message
   client.connect(broker)
   mqtt_looping = True
   print "Looping..."
   cnt = 0
   while mqtt_looping:
     client.loop()
     cnt+=1
     if cnt>50:
       try:
         client.reconnect()
       except:
         time.sleep(1)
       cnt = 0
   client.disconnect

mqtt_device_sub()

