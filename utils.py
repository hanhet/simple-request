import fcntl,socket, struct
import commands
import getmac
def getHwAddr():
    return getmac.get_mac_address()
    #s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #info = fcntl.ioctl(s.fileno(), 0x8927, struct.pack('256s', ifname[:15]))
    #return ':'.join(['%02x' % ord(char) for char in info[18:24]])
def getAddress(addresses):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('google.com', 0))
    ipAddress = s.getsockname()[0]
    s.close()
    return  ipAddress
