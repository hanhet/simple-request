import os
import time
import psutil
import sys
import atexit

def GetMemorystate():
    phymem = psutil.virtual_memory()
    string = str(int(phymem.total / 1024 /1024))+"M"
    #string += "-"
    #string += str(int(phymem.used / 1024 / 1024))+"M"
    #string += "-"
    #string += str(int(phymem.free / 1024 / 1024))+"M"
    #string += "-"
    return (string)

