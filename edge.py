import sys, os, time, signal
import json
import base64
import paho.mqtt.client as mqtt

reload(sys)
sys.setdefaultencoding('utf-8')

client = None
mqtt_looping = False

topic = 'hanhet/simple-request'
compose_file = 'rcvtest.yml'
client_id = ""
username = ""
password = ""

def on_connect(mq, userdata, rc, _):
   #subscribe when connected.
   mq.subscribe(topic, qos=2)

def on_message(mq, userdata, msg):
   #print "topic: %s" % msg.topic
   #print "payload: %s" % msg.payload
   print "qos: %d" % msg.qos
   js = json.loads(msg.payload)
   #print(type(js))
   fp = open(compose_file, "w")
   #print js.get('req')
   decode = base64.b64decode(js.get('req'))
   #print decode
   fp.write(decode)
   #write decode base64 data out to test3.yml
   fp.close()

def mqtt_client_thread():
   global client,mqtt_looping
   client = mqtt.Client(client_id=client_id)
   
   # If broker asks user/password.
   client.username_pw_set(username, password)
   #auth = {'username': "", 'password': ""}
   client.on_connect = on_connect
   client.on_message = on_message

   try:
       client.connect("broker.hivemq.com")
   except:
       print "MQTT Broker is not online. Connect later."

   mqtt_looping = True
   print "Looping..."

   #mqtt_loop.ioop_forever()
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

if __name__ == '__main__':
    signal.signal(signal.SIGTERM, stop_all)
    signal.signal(signal.SIGQUIT, stop_all)
    signal.signal(signal.SIGINT, stop_all)

    mqtt_client_thread()
    print "exit program"
    sys.exit(0) 
