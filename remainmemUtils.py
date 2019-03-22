import os
import time
import psutil
import sys
import atexit

def GetRemainMemorystate():
	phymem=psutil.virtual_memory()
	string = str(int(phymem.free /1024 /1024))+"M"
	#string += "-"
	return (string)
