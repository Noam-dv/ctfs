# thought process

going over the code theres an obvious bof on input[100] which is a global. the issue is input is checked with "daehee" so we have to somehow bypass that check. or this may be a redhairing.

looking back and reading the doc, strncmp gets 6 here so it only reads the first 6 chars so it should be fine to overwrite. (aslong as we keep the first 6 chars the str its compared to)

the page is always at the same base offset so maybe i can use that but i doubt thatll be consistent.

all the registers are set to 0x1000 + plus their random number but in the bounds of the page so theres no issue

my current direction is to read the values on the script determine where they point and overwrite those registers and especially eax to run a syscall that could give me shell. the main ones such as execv and fork are blocked so ill have to read about more.
