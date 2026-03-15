**Thought Proccess**

we have col elf and col.c
the binary recieves a pasword, runs some algorithm on it and compares it to 0x21DD09EC
pass must be 20 bytes

seems we have to reverse engineer this password

```
unsigned long check_password(const char* p){
  int* ip = (int*)p;
  int i;
  int res=0;
  for(i=0; i<5; i++){
    res += ip[i];
  }
  return res;
}

```

this function recieves our 20 byte long input and then gets checked with 0x21DD09EC
basically we need to enter 20 chars, that their sum when casted to an int, is equal to 0x21DD09EC
1 char = 1 byte, 1 int = 4 bytes
so thats why it loops over 5 ints
we must get 20 chars split into 5 groups, whos sum wold be 0x21DD09EC (decimal is 568,134,124)
the cast to int* is signed so the max would be 2,147,483,647
i must find the representation of 568,134,124 in binary then turn each 8 bits to a char
`00100001 11011101 00001001 11101100 `

now lets get the value of each byte as a number and get its ascii char
it would be ! \xDD \t \xEC
and ill print an additonal 16 null bytes which ahve the ascii value of 0

i will make a python script to generate the output

after testing i realize thag argv strings cant have null bytes cuz theyll stop reading the string
so lets just do 568,134,124 / 5  ( its a decimal num so nvm )
lets just get 4 numbers and calc the fifth
for example lets get 100,000,000 * 4
and then calculate the last number
= 168,134,124

now lets represent 100,000,000 in binary
00000101 11110101 11100001 00000000

lets get the char for each block

once again a nul byte so they cant be in a string
lets use A for example

`ip0 = ip1 = ip2 = ip3 = 0x41414141`

`ip4 = 0x21DD09EC - 0x05050504 = 0x1CD804E8`

so the output would be A * 16 and then b"\xe8\x04\xd8\x1c" (little endian)

it worked! Two_hash_collision_Nicely
