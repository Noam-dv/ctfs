import subprocess

path = "/home/ascii_easy/libc-2.15.so"
base = 0x5555e000
def is_ascii(addr):
    b = addr.to_bytes(4, 'little') #little endian
    return all(0x20 <= x <= 0x7e for x in b)

#ropper not installed on the server
#run ropper
#result = subprocess.check_output(
#    ["ropper", "--file", path, "--nocolor"],
#    text=True
#)
result = subprocess.check_output(
    ["ROPgadget", "--binary", path],
    text=True
)   

good_gadgets = []
for line in result.splitlines():
    if ":" not in line:
        continue
    try:
        offset_str,gadget = line.split(":", 1)
        offset = int(offset_str.strip(), 16)
    except:
        continue

    real_addr = base+offset
    if is_ascii(real_addr):
        good_gadgets.append((real_addr, gadget.strip()))
print(f"---found {len(good_gadgets)} ascii printable gadgets:\n")

with open("gadgets_ascii.txt", "w") as f:
    for addr,gadget in good_gadgets:
        f.write(f"{hex(addr)} : {gadget}\n")