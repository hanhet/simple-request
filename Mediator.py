import sys, os, time, signal
import json
import paho.mqtt.client as mqtt
import unicodedata

reload(sys)
sys.setdefaultencoding('utf-8')

client = None
prefix = 'ucan_coo'
topic = prefix+'/register/request'
topic_d = prefix+'/search/request'
client_id = ""
username = ""
password = ""
broker = "broker.hivemq.com"
edge_capability = {}
count=0
connect_status = False

def on_connect(mq, userdata, flags, rc):
   print 'Connect: ' + str(rc)
   if rc == 0:
      print 'Mediator started ...'
      connect_status = True
      mq.subscribe(topic, qos=2)
      mq.subscribe(topic_d, qos=2)
   else:
      print 'Shutting down mediattor'
      exit()

def on_message(mq, userdata, msg):
   rx_topic = msg.topic
   print rx_topic
   if rx_topic == topic: # register/request
      dictstr = json.dumps(json.loads(msg.payload),ensure_ascii=False,encoding='utf-8')
      dict = json.loads(dictstr)
      if dict.get('disk') == None:
        payload = 100
        print 'A'
      elif dict.get('memory') == None:
        payload = 100
      else:
        payload = 200
      client__id = dict['client_id']
      tx_topic = prefix+'/register/response/'+client__id
      client.publish(tx_topic,payload,qos=2,retain=False)
      remaindisk = (dict['disk']['remaindisk'])
      totaldisk = (dict['disk']['totaldisk'])
      remainmem = (dict['memory']['remainmem'])
      totalmem = (dict['memory']['totalmem'])
      edge_capability[client__id]={}
      edge_capability[client__id]['disk']=dict['disk']
      edge_capability[client__id]['memory']=dict['memory']
      print edge_capability

   if rx_topic == topic_d: # search/request
      dictstr = json.dumps(json.loads(msg.payload),ensure_ascii=False,encoding='utf-8')
      dict = json.loads(dictstr)
      # select edge
      if dict.get('disk') == None:
         payload = 100
         print "A"
      elif dict.get('memory') == None:
         payload = 100
         print "B"
      else:
         payload = 200
         print "C"
      client__id = dict['client_id']
      tx_topic = prefix+'/search/response/'+client__id
      client.publish(tx_topic,payload,qos=2,retain=False)
      remaindisk = (dict['disk']['remaindisk'])
      remainmem = (dict['memory']['remainmem'])
      
def start_mediator():
   print 'Starting mediator ...'
   global client,mqtt_looping
   client = mqtt.Client(client_id=client_id)
   client.username_pw_set(username,password)
   client.on_connect = on_connect
   client.on_message = on_message
   client.connect(broker)
   mqtt_looping = True
   # print "Looping..."
   cnt = 0
   while mqtt_looping:
     client.loop()
     
     cnt +=1
     if cnt >50:
       try:
         client.reconnect()
       except:
         time.sleep(1)
       cnt = 0
   client.disconnect()

start_mediator()
