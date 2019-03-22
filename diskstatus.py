import os
import time
import psutil
import sys
import atexit

def GetDiskstate():
    diskinfo = psutil.disk_usage('/')
    disk_str = str(int(diskinfo.total/1024/1024/1024))+"G"
    #disk_str += "-"
    #disk_str += str(int(diskinfo.used/1024/1024/1024))+"G"
    #disk_str += "-"
    #disk_str += str(int(diskinfo.free/1024/1024/1024))+"G"
    return (disk_str)
