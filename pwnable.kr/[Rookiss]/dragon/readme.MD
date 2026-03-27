# Solution + Thought Process

UNFINISHED (spent 20 m and had to leave)





"I made a RPG game for my little brother.
But to trick him, I made it impossible to win.
I hope he doesn't get too angry with me"

```
dragon@ubuntu:~$ cat readme
once you connect to port 9004, the "dragon" binary will be executed under dragon_pwn privilege.
make connection to challenge (nc 0 9004) then get the flag
```

lets checsec and file

![1774607227816](images/readme/1774607227816.png)

nice, ill run the binary once jsut to see how it behaves and then put it into ghidra.

![1774607361796](images/readme/1774607361796.png)

Wow its litterally an entire game. this will probably be hard to reverse and engineer and exploit. ill start by opening it in ghidra.

alright lets start from the begining. _start() initializes the program and the canary, now ill check the main function.

![1774607759820](images/readme/1774607759820.png)

super straight forward just prints welcome and starts the game.

![1774607792803](images/readme/1774607792803.png)

as we can see play game just checks what character we want to pick and then starts the dragon fight. if we pick 3 we get a secret level :,) lets see what get choice does, what fight dragon does and then well get to the secret level.

![1774607922844](images/readme/1774607922844.png)

seems simple enough, reads input and cleans the buffer of \n. fight dragon is where it gets real, ill interepret it as chunks

![1774608242979](images/readme/1774608242979.png)

first of all i renamed the param to player as thats what we pass, we allocate some memory and do an AND operator with count (a global variable) and check if its 0 (as in counts lsb is 0 so its even) if the lsb is even it adds 1 to count, sets the some elements in the allocated memory. basically what ithink this does is switchese between the baby dragon and the mama dragon with each turn as i saw happend when i played the game. full block of code:

![1774608469040](images/readme/1774608469040.png)

the next chunk of code i believe initalizes some player info

![1774608684763](images/readme/1774608684763.png)

ptr[1] most likely holds the players health as the priest starts with 42 health (i noticed when i played) and the knight starts with 50. im unsure what ptr[2] is ill check on the game.

![1774608787470](images/readme/1774608787470.png)

seems like ptr[2] holds mana points. ill rename ptr to player_info.

![1774608920061](images/readme/1774608920061.png)

back tracking i can now pretty much understand what puVar1 holds. as ssen in the baby dragon stats it has 50 hp 30 damage and 5 life regen so ill rename it to enemy_info
