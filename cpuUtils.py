import os
import time
import psutil
import sys
import atexit


def GetCPUstate(time_count = 1):
    return (str(psutil.cpu_count(logical=True))+"-"+str(psutil.cpu_percent(time_count,0)) + "%")

def GetCPUstatus(time_count=1):
    return (str(psutil.cpu_percent(time_count,1)) + "%")
