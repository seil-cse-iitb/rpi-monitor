import json
import os
import re

conf=json.load(open("config.json"))
msg={}

def get_rpi_details():
    msg['rpi_time'] = os.popen("date").read()
    msg['up_time']  = os.popen("uptime -p").read()
    msg['up_since'] = os.popen("uptime -s").read()

    result=os.popen("egrep 'Mem|Cache|Swap' /proc/meminfo | awk '{print $2}").read().split('\n')
    msg['memory_total'] =  result[0]
    msg['memory_free'] =  result[1]
    msg['memory_available'] =  result[2]
    msg['cached'] =  result[3]
    msg['swap_cached'] =  result[4]
    msg['swap_total'] =  result[5]
    msg['swap_free'] =  result[6]


    result= os.popen("cat /proc/loadavg").read().split(' ')
    msg['load 1_min']=result[0]
    msg['load 5_min']=result[1]
    msg['load 15_min']=result[2]

    msg['users']=os.popen("uptime | awk '{print $6}'")

    print (msg)

def get_process_stat():
    process_to_monitor=config['process']
    print process_to_monitor
    call(["ls", "-l"])
    return 0


def get_service_stat():
    t=call(["uptime"])
    return t


get_process_stat()
#
# get_rpi_details()

# def main():

#
#
# if __name__ == "__main__":
#     try:
#         conf = json.load(open("config_main.json"))
#     except :
#         print ("Error opening conf file")
#     main()
