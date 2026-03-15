### Thought Process

The binary takes in a number X, calculates X - 0x1234, then it calls read on the num passing it as the file descriptor.
The read function stores 32 bytes in the buf and compares the buf to "letmewin"
fd 0 would be stdin so i can write in the input 0x1234, then the fd would be 0x1234 - 0x1234 = 0
The program would then read 32 bytes from stdin and i can just write the str it strcmps to
0X1234 = 4460 In decimal
fd@ubuntu:~$ ./fd 4660
LETMEWIN
good job :)
Mama! Now_I_understand_what_file_descriptors_are!

it worked!
