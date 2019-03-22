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

broker = 'broker.hivemq.com'
topic = 'register/request'
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
req_id = utils.getHwAddr('eth0')+utils.getAddress('adr')
print req_id
hash_id = hmac.new(key,req_id, hashlib.sha1)
signature = hash_id.hexdigest()
print signature

data = {"client_id":signature,"memory":[{"totalmem":totalmemoryperformance,"remainmem":remainmemoryperformance}],"disk":[{"totaldisk":totaldiskcapcity,"remaindisk":remaindiskcapcity}]}

#print data
payload = json.dumps(data)
print payload
client.connect(broker, keepalive=60,bind_address="")
client.publish(topic,"%s" % payload,qos=2,retain = True)
