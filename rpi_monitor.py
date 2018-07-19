import json
import os
import re

conf=""
msg={}

def get_rpi_details():
    msg['rpi_time'] = os.popen("date").read()
    msg['up_time']  = os.popen("uptime -p").read()
    msg['up_since'] = os.popen("uptime -s").read()

    result=os.popen("egrep 'Mem|Cache|Swap' /proc/meminfo").read().split('\n')
    msg['memory_total'] =  result[0].split(' ')[-2]
    msg['memory_free'] =  result[1].split(' ')[-2]
    msg['memory_available'] =  result[2].split(' ')[-2]
    msg['cached'] =  result[3].split(' ')[-2]
    msg['swap_cached'] =  result[4].split(' ')[-2]
    msg['swap_total'] =  result[5].split(' ')[-2]
    msg['swap_free'] =  result[6].split(' ')[-2]


    result= os.popen("cat /proc/loadavg").read().split(' ')
    msg['load 1_min']=result[0]
    msg['load 5_min']=result[1]
    msg['load 15_min']=result[2]

    # result=os.popen("df | grep 'root'").read().split(' ')

    print (msg)

def get_process_stat():
    call(["ls", "-l"])
    return 0


def get_service_stat():
    t=call(["uptime"])
    return t


get_rpi_details()

# def main():

#
#
# if __name__ == "__main__":
#     try:
#         conf = json.load(open("config_main.json"))
#     except :
#         print ("Error opening conf file")
#     main()
