import os
import time
import psutil
import sys
import atexit

def GetremainDiskcapcity():
	diskinfo = psutil.disk_usage('/')
	disk_str = str(int(diskinfo.free/1024/1024/1024))+"G"
	return (disk_str)
