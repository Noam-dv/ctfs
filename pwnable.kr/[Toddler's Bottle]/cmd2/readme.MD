## Thought Process

```
#include <stdio.h>
#include <string.h>

int filter(char* cmd){
	int r=0;
	r += strstr(cmd, "=")!=0;
	r += strstr(cmd, "PATH")!=0;
	r += strstr(cmd, "export")!=0;
	r += strstr(cmd, "/")!=0;
	r += strstr(cmd, "`")!=0;
	r += strstr(cmd, "flag")!=0;
	return r;
}

extern char** environ;
void delete_env(){
	char** p;
	for(p=environ; *p; p++)	memset(*p, 0, strlen(*p));
}

int main(int argc, char* argv[], char** envp){
	delete_env();
	putenv("PATH=/no_command_execution_until_you_become_a_hacker");
	printf("before:   %s\n", argv[1]);
	if(filter(argv[1])) return 0;
	printf("%s\n", argv[1]);
	system( argv[1] );
	return 0;
}

```



After viewing the file, i see a similar challange as in CMD1, except with more filters. this time around, we are unable to simply write an absolute path as they block "/" and we cant inject a new path cuz they block "=" and "PATH"

We have a delete env variable function, which would solve our problem and allow us to Cat the flag. Perhaps we have to jump to it somehow? Maybe we can encode the letters that are blocked somehow? I believe that wont work cause we cast the bytes to a char anyway. The environment is completely wiped, so ill check what commands are built in (we can actually use). Theres a big list of commands such as read, exec, kill etc. what caught my eye is echo. the filter does not block redirects so maybe we can echo the contents of all the files in the folder? (using the * operator and stdio redirections)

currently my direction is using the read command "read fl < flag; echo $fl" something like this. i think this would work but i need to find a way to redirect flag cuz when i do f* it doesnt seem to unpack in the shell. (it does usually, but maybe because i stringified it, not sure".

after testing a bit, i realize i can do read fl < stdin; echo fl and itll let me write a command and it wont be filtered, so i can simply do /bin/cat flag and itll cat the flag, store it in fl, and print fl. theres no need to do < stdin becuase thats the default so ill just write `read fl; echo $fl ` and then when i get input ill write `/bin/cat ./f*`. it didnt work and after reading a bit i realized that f* didnt get run because i didnt put it in the substitution operator. add $() to actually run the command inside. so behind the scenes my command read fl; echo fl will get run and the output of that will get substituted into the shell the program creates. the output of that would be whatever i type (because it js echos stdin) and then i can write /bin/cat ./flag
