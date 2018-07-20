import json
import os
import socket
import time
import paho.mqtt.client as mqtt
import thread

conf=my_ip=mqtt_host=mqtt_port=mqtt_keepalive=mqtt_topic_publish=mqtt_qos=mqttc=interval=""
rpi_stat={}
process_stat={}
service_stat={}

def get_my_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    my_ip=s.getsockname()[0]
    s.close()


def get_rpi_stat():
    rpi_stat['rpi_time'] = os.popen("date").read()

    rpi_stat['up_time']  = os.popen("uptime -p").read()

    rpi_stat['up_since'] = os.popen("uptime -s").read()

    result=os.popen("egrep 'Mem|Cache|Swap' /proc/meminfo | awk '{print $2}'").read().split('\n')
    rpi_stat['memory_total'] =  result[0]
    rpi_stat['memory_free'] =  result[1]
    rpi_stat['memory_available'] =  result[2]
    rpi_stat['cached'] =  result[3]
    rpi_stat['swap_cached'] =  result[4]
    rpi_stat['swap_total'] =  result[5]
    rpi_stat['swap_free'] =  result[6]

    result= os.popen("cat /proc/loadavg").read().split(' ')
    rpi_stat['load 1_min']=result[0]
    rpi_stat['load 5_min']=result[1]
    rpi_stat['load 15_min']=result[2]

    rpi_stat['users']=os.popen("uptime | awk '{print $6}'").read()



def get_process_stat():
    process_to_monitor=conf['process']
    for process in process_to_monitor:
        process_stat[process]=os.popen("ps aux | grep "+str(process) +" | wc -l").read()



def get_service_stat():
    service_to_monitor=conf['service']
    for service in service_to_monitor:
        s={}
        s['status']=os.popen("sudo service  "+str(service) +" status  | grep Active | awk '{print $6 $7}'").read()
        s['since']=os.popen("sudo service  "+str(service) +" status  | grep Active | awk '{print $2}'").read()
        service_stat[service]=s


def publish_stat():
    class_room="test/"
    mqttc.publish(mqtt_topic_publish+class_room+"rpi_stat",str(rpi_stat),mqtt_qos)
    mqttc.publish(mqtt_topic_publish+class_room+"process_stat",str(process_stat),mqtt_qos)
    mqttc.publish(mqtt_topic_publish+class_room+"service_stat",str(service_stat),mqtt_qos)


def collect():
    while(True):
        get_rpi_stat()
        get_process_stat()
        get_service_stat()
        publish_stat()
        time.sleep(interval)


def request_handeler():
    class_room="test"
    def on_connect(client, userdata, flags, rc):
        client.subscribe(mqtt_topic_req+class_room)

    def on_message(client, userdata, msg):
        print (msg.payload)
        get_rpi_stat()
        get_process_stat()
        get_service_stat()
        publish_stat()


    client_sub = mqtt.Client(protocol=mqtt.MQTTv31)
    client_sub.on_connect = on_connect
    client_sub.on_message = on_message
    client_sub.connect(mqtt_host,mqtt_port,mqtt_keepalive)
    client_sub.loop_forever()




if __name__ == "__main__":

    try:
        conf = json.load(open("config.json"))
    except :
        print ("Error opening config.json File")

    my_ip=get_my_ip
    interval=conf['interval']
    mqtt_host=conf['mqtt_host']
    mqtt_port=conf['mqtt_port']
    mqtt_keepalive=conf['mqtt_keepalive']
    mqtt_topic_publish=conf['mqtt_topic_publish']
    mqtt_topic_req=conf['mqtt_topic_req']
    mqtt_qos=conf['mqtt_qos']
    mqttc=mqtt.Client("Rpi-Monitor: "+str(my_ip))
    mqttc.connect(mqtt_host,mqtt_port,mqtt_keepalive)


    try:
        thread.start_new_thread(collect,())
        thread.start_new_thread(request_handeler,())
    except Exception as  e:
        print(e)

    while True:
        pass
