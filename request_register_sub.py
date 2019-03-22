import sys, os, time, signal
import json
import paho.mqtt.client as mqtt
#import unicodedata

reload(sys)
sys.setdefaultencoding('utf-8')

client = None
mqtt_looping = False

topic = 'register/request'
client_id = ""
username = ""
password = ""

def on_connect(mq, userdata, rc, _):
   mq.subscribe(topic, qos=2)

def on_message(mq, userdata, msg):
   print "qos: %d" % msg.qos
   print type(msg) 
   dict = json.dumps(json.loads(msg.payload))
   print dict
   print type(dict)
   dict2 = json.loads(dict)   
   #print dict2
   #print type(dict2)
   #totaldisk =  (dict2['disk'][0]['totaldisk'])
   #totaldiskconvertostr = totaldisk.encode('utf-8')
   #print type(totaldiskconvertostr)
   client__id = (dict2['client_id'])
   client__idconvertostr = client__id.encode('utf-8')
   print client__idconvertostr
   remaindisk = (dict2['disk'][0]['remaindisk'])
   remaindiskconvertostr = remaindisk.encode('utf-8')
   print remaindiskconvertostr
   totaldisk = (dict2['disk'][0]['totaldisk'])
   totaldiskconvertostr = totaldisk.encode('utf-8')
   print totaldiskconvertostr
   remainmem = (dict2['memory'][0]['remainmem'])
   remainmemconvertostr = remainmem.encode('utf-8')
   print remainmemconvertostr
   totalmem = (dict2['memory'][0]['totalmem'])
   totalmemconvertostr = totalmem.encode('utf-8')
   print totalmemconvertostr
   dictedgedatabase = {}
   print type(dictedgedatabase)
   dictedgedatabase.update({client__idconvertostr:{'memory':[{'totalmem':totalmemconvertostr,'remainmem':remainmemconvertostr}]},'disk':[{'totaldisk':totaldiskconvertostr,'remaindisk':remaindiskconvertostr}]})
   print dictedgedatabase
def mqtt_client_thread():
   global client,mqtt_looping
   client = mqtt.Client(client_id=client_id)
   client.username_pw_set(username,password)
   client.on_connect = on_connect
   client.on_message = on_message
 
   try:
      client.connect("broker.hivemq.com")
   except:
      print "MQTT Broker is not online. Connect later"

   mqtt_looping = True
   print "Looping..."
   
   cnt = 0
   while mqtt_looping:
      client.loop()

      cnt +=1
      if cnt > 200:
         try:
            client.reconnect()
         except:
            time.sleep(1)
         cnt = 0

   print "quit mqtt thread"
   client.disconnect()

def stop_all(*args):
   global mqtt_loopinf
   mqtt_looping = False

if __name__=='__main__':
   signal.signal(signal.SIGTERM, stop_all)
   signal.signal(signal.SIGQUIT, stop_all)
   signal.signal(signal.SIGINT, stop_all)
   
   mqtt_client_thread()
   print "exit program"
   sys.exit(0)
