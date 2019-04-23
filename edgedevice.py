import atexit
import sys, os, time 
import json
import base64 
import paho.mqtt.client as mqtt
import paho.mqtt.publish
import utils
import hashlib
import hmac
import cpuUtils
import memUtils
import remainmemUtils
import diskstatus
import remaindiskcapcityUtils

reload(sys) 
sys.setdefaultencoding('utf-8')
client = None
prefix = 'ucan_coo'
broker = "broker.hivemq.com"
topic = prefix+'/register/request'
compose_file = 'test.yml'
payload = ""
msg = ""
key = 'signature is unique'
hash_id= "" 
count=0
# If broker asks client id
client_id = ""
client = mqtt.Client(client_id=client_id)

# If broker asks user/password
username = ""
password = ""
client.username_pw_set(username, password)

cpu = cpuUtils.GetCPUstate(time_count=1)+cpuUtils.GetCPUstatus(time_count=1)
print cpu
totalmemoryperformance = memUtils.GetMemorystate()
print totalmemoryperformance
remainmemoryperformance = remainmemUtils.GetRemainMemorystate()
print remainmemoryperformance
totaldiskcapcity = diskstatus.GetDiskstate()
print totaldiskcapcity
remaindiskcapcity = remaindiskcapcityUtils.GetremainDiskcapcity()
print remaindiskcapcity
# Generate service id
req_id = utils.getHwAddr()+utils.getAddress('adr')
print req_id
hash_id = hmac.new(key,req_id, hashlib.sha1)
signature = hash_id.hexdigest()
print signature

data = {"client_id":signature,"memory":{"totalmem":totalmemoryperformance,"remainmem":remainmemoryperformance},"disk":{"totaldisk":totaldiskcapcity,"remaindisk":remaindiskcapcity}}
#data = {"client_id":signature}
#print data
payload = json.dumps(data)

#client.connect(broker, keepalive=60,bind_address="")
#client.publish(topic,payload,qos=2,retain = False)
#print topic
topic2 = prefix+'/register/response/'+signature
#print topic2

def on_publish(client, userdata, mid):
    print 'pub ok'

def on_connect(mq, userdate, flags, rc):
   print rc
   print topic
   print payload
   mq.publish(topic,payload,qos=2)
   mq.subscribe(topic2, qos=2)

def on_message(mq, userdate, msg):
   print msg.topic
   print msg.payload

def start_register():
   global client, mqtt_looping
   client = mqtt.Client(client_id=client_id)
   client.username_pw_set(username,password)
   client.on_connect = on_connect
   client.on_message = on_message
   #client.on_publish = on_publish
   client.connect(broker)
   mqtt_looping = True
   print "Looping..."
   cnt = 0
   while mqtt_looping:
      client.loop()

      cnt +=1
      if cnt > 50:
        try:
          client.reconnect()
        except:
          time.sleep(1)
        cnt = 0
   client.disconnect()

start_register()
