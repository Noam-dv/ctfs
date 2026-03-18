# Thought Process

Connecting to the server i see a few files (Dockerfile, super.pl) the binary, and a readme. the readme simply explains how to run the binary (netcat) and to try crack the calculator. i want to understand what this md5calculator does but we are not given the source code. ill start by running file and checksec on it

![1773827707949](images/readme/1773827707949.png)

No aslr and its not stripped!!! my life has been made a lot easier. ill download this file to my computer using scp and put it into ghidra.         After letting ghidra identify functions i see a main, ill start from the begining and check what it does. we can also so a custom hash implementation, but we'll get to that later.

![1773828162024](images/readme/1773828162024.png)

```
undefined4 main(void)

{
  uint __seed;
  int local_18;
  int local_14;
  
  setvbuf(stdout,(char *)0x0,1,0);
  setvbuf(stdin,(char *)0x0,1,0);
  puts("- Welcome to the free MD5 calculating service -");
  __seed = time((time_t *)0x0);
  srand(__seed);
  local_14 = my_hash();
  printf("Are you human? input captcha : %d\n",local_14);
  __isoc99_scanf(&DAT_080492df,&local_18);
  if (local_14 != local_18) {
    puts("wrong captcha!");
                    /* WARNING: Subroutine does not return */
    exit(0);
  }
  puts("Welcome! you are authenticated.");
  puts("Encode your data with BASE64 then paste me!");
  process_hash();
  puts("Thank you for using our service.");
  system("echo `date` >> log");
  return 0;
}

```

The puts calls make this a lot easier to understand, as we can see we have to identify ourselves by copying the hash thats calculated? the print casts local_14 to a int, later ill check what my_hash returns.  after authenticating i see we get to mayb run our own input through the hash function? ill go ahead and check what my_hash() does.

```
int my_hash(void)
{
  int iVar1;
  int in_GS_OFFSET;
  int local_3c;
  int local_30 [4];
  int local_20;
  int local_1c;
  int local_18;
  int local_14;
  int local_10;
  
  local_10 = *(int *)(in_GS_OFFSET + 0x14);
  for (local_3c = 0; local_3c < 8; local_3c = local_3c + 1) {
    iVar1 = rand();
    local_30[local_3c] = iVar1;
  }
  if (local_10 != *(int *)(in_GS_OFFSET + 0x14)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return local_1c + local_30[1] + (local_30[2] - local_30[3]) + local_10 + local_14 +
         (local_20 - local_18);
}
```

my hash uses a bunch of unitialized integers to calculate a sort of pseudo random number (a predictable random, no randomized seed is used) and returns an int. i dont see a reason why inputting the string thats printed wouldnt work. ill try.

![1773828776302](images/readme/1773828776302.png)

that was slighlty easier than i expected, i probably wasted some time on a red hairing. anyway ill continue on to the hash itself. ill go ahead and read process_hash() which is the next function called by main.


## process_hash()

This is the main function of this ctf. the code is very obfuscated in a attempt to throw me off.

##### **I Have renamed the variable names to make it more clear whats going on :**

```
void process_hash(void)

{
  undefined4 decodedLen;
  void *md5result;
  int loopCount;
  undefined4 *bufferPtr;
  int gsOffset;
  byte zero;
  undefined4 decodedBuffer [128];
  int stackCanary;
  
  zero = 0;
  stackCanary = *(int *)(gsOffset + 0x14);
  bufferPtr = decodedBuffer;
  for (loopCount = 0x80; loopCount != 0; loopCount = loopCount + -1) {
    *bufferPtr = 0;
    bufferPtr = bufferPtr + 1;
  }
  do {
    loopCount = getchar();
  } while (loopCount != 10);
  bufferPtr = &g_buf;
  for (loopCount = 0x100; loopCount != 0; loopCount = loopCount + -1) {
    *bufferPtr = 0;
    bufferPtr = bufferPtr + (uint)zero * -2 + 1;
  }
  fgets((char *)&g_buf,0x400,stdin);
  bufferPtr = decodedBuffer;
  for (loopCount = 0x80; loopCount != 0; loopCount = loopCount + -1) {
    *bufferPtr = 0;
    bufferPtr = bufferPtr + (uint)zero * -2 + 1;
  }
  decodedLen = Base64Decode(&g_buf,decodedBuffer);
  md5result = (void *)calc_md5(decodedBuffer,decodedLen);
  printf("MD5(data) : %s\n",md5result);
  free(md5result);
  if (stackCanary != *(int *)(gsOffset + 0x14)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}

```

Ill try explain the code block by block:

First of all, the stack canary that the compiler put in is saved to a variable in order to check if i messed with the stack later on.

```
  zero = 0;
  stackCanary = *(int *)(gsOffset + 0x14);
  bufferPtr = decodedBuffer;
```

Next all the buffers are zerod out. this looks confusing as i believe that was the intention, but the code is fundementally simple once you disect it and rename variables (crutially the `zero` variable)

```
  for (loopCount = 0x80; loopCount != 0; loopCount = loopCount + -1) {
    *bufferPtr = 0;
    bufferPtr = bufferPtr + 1;
  }
  do {
    loopCount = getchar();
  } while (loopCount != 10);
  bufferPtr = &g_buf;
  for (loopCount = 0x100; loopCount != 0; loopCount = loopCount + -1) {
    *bufferPtr = 0;
    bufferPtr = bufferPtr + (uint)zero * -2 + 1;
  }
```

as we can see the program also loops over all chars entered till i give a newline char ```loopcount != 10``` in order to setup the fgets call and make sure it gets a clean input. an example of some obfuscation here meant to make the code not understandable is the ```bufferptr = bufferptr + (uint)zero * -2 + 1``` which essentially is just ```bufferptr = bufferptr + 1```. renaming the variables helped out here a lot.

Next the base64 encoded string is inputted into g_buf which ig is just a global buffer and then decoded and put into decodedbuffer. Once again decodedbuffer is zerod out here in a weird way but its the same thing as earlier.

```
  fgets((char *)&g_buf,0x400,stdin);
  bufferPtr = decodedBuffer;
  for (loopCount = 0x80; loopCount != 0; loopCount = loopCount + -1) {
    *bufferPtr = 0;
    bufferPtr = bufferPtr + (uint)zero * -2 + 1;
  }
  decodedLen = Base64Decode(&g_buf,decodedBuffer);
```

and lastly, we put it through MD5, print the result and check the stack canary before the return.

```
  md5result = (void *)calc_md5(decodedBuffer,decodedLen);
  printf("MD5(data) : %s\n",md5result);
  free(md5result);
  if (stackCanary != *(int *)(gsOffset + 0x14)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
```


Since theres the usage of the canary my inital insticnt is to look for a buffer overflow. i first attempted to find the size of g_buf to see if fgets was recieving too much data, but then i noticed that g_bufs size is 1024 and decoded buffers size is 128 * 4 = 512. im unsure of how base 64 so im going to ask claude if thats a product of decoding from base64 or if thats a vulnerability. a base64 decoded string of 1024 bytes can resolve to upto roughly 768 bytes meaning theres ++++a clear overflow here. i need to find a way to get the canarys value though so i dont change it. what im thinking is to put a breakpoint when the canary is put into a variable so i can see it on the stack but that kind of feels like cheating. it wont work regardless cuz we have to nc to run the program and its not local. maybe we have to leak it somehow. i also dont see any print flag here lol, maybe we need to overwrite the string thats called into system() to make it say like cat ./flag or something.


After looping back to the my_hash() function i see that the canary is infact used there in the calculation, we could probably get all the random values and then calculate the canary on runtime and then overflow the buffer simply
