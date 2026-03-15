## Thought Process

```
asm@ubuntu:~$ ls
asm
asm.c
readme
this_is_pwnable.kr_flag_file_please_read_this_file.sorry_the_file_name_is_very_loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000000000000ooooooooooooooooooooooo000000000000o0o0o0o0o0o0ong
```

Extremely weird naming conventions lol. Ill check out the readme

```
#define LENGTH 128

void sandbox(){
        scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_KILL);
        if (ctx == NULL) {
                printf("seccomp error\n");
                exit(0);
        }

        seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(open), 0);
        seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
        seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
        seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);
        seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0);

        if (seccomp_load(ctx) < 0){
                seccomp_release(ctx);
                printf("seccomp error\n");
                exit(0);
        }
        seccomp_release(ctx);
}

char stub[] = "\x48\x31\xc0\x48\x31\xdb\x48\x31\xc9\x48\x31\xd2\x48\x31\xf6\x48\x31\xff\x48\x31\xed\x4d\x31\xc0\x4d\x31\xc9\x4d\x31\xd2\x4d\x31\xdb\x4d\x31\xe4\x4d\x31\xed\x4d\x31\xf6\x4d\x31\xff";
unsigned char filter[256];
int main(int argc, char* argv[]){

        setvbuf(stdout, 0, _IONBF, 0);
        setvbuf(stdin, 0, _IOLBF, 0);

        printf("Welcome to shellcoding practice challenge.\n");
        printf("In this challenge, you can run your x64 shellcode under SECCOMP sandbox.\n");
        printf("Try to make shellcode that spits flag using open()/read()/write() systemcalls only.\n");
        printf("If this does not challenge you. you should play 'asg' challenge :)\n");

        char* sh = (char*)mmap(0x41414000, 0x1000, 7, MAP_ANONYMOUS | MAP_FIXED | MAP_PRIVATE, 0, 0);
        memset(sh, 0x90, 0x1000);
        memcpy(sh, stub, strlen(stub));

        int offset = sizeof(stub);
        printf("give me your x64 shellcode: ");
        read(0, sh+offset, 1000);

        alarm(10);
        chroot("/home/asm_pwn");        // you are in chroot jail. so you can't use symlink in /tmp
        sandbox();
        ((void (*)(void))sh)();
        return 0;
}
```

Seems like were put in a sandbox where i can only use very basic syscalls. the goal is to pass raw bytes into executable memory.`read(0, sh+offset, 1000);` the program reads raw bytes from stdin into executable memory. I believe i have to create a program that somehow reads the file and writes it to stdout. Ill start by reading more about the syscalls i have access too, what they take in, what they recieve and perhaps how to write a small program without needing to write directly the assembly.

### open: 

the open syscall recieves a filename and flags (Read Only, Write Only, Create if doesnt exist, etc). the function returns the File descriptor to the file. `open(const char  *pathname, int flags);` this function will utilize us opening the flag file in memory.

### read:

The read syscall recieves a file descriptor fd, a buffer and a max size X, and reads X bytes from fd into the buffer. Read returns the amount of bytes actually read. read increments the file position accordingly so you can read 16 from X and then read the next 16 easily. `ssize_t read(int fd, void* buf, size_t count);`

### write:

the Write syscall recieves a file descriptor a buffer and a size and writes X bytes from the buffer into the file. this can be used to write to stdout (fd 1) very easily!!! in our case we will use all 3 syscalls i wrote about to read the contents from the flag file and write it to stdout


Instead of writing raw assembly, ill use shellcraft from pwntools which generates the shellcode for me from simple instructions.
