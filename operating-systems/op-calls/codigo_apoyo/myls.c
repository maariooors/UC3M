//P1-SSOO-23/24

#include <stdio.h>		  /* Header file for system call printf */
#include <unistd.h>		  /* Header file for system call gtcwd */
#include <dirent.h>       /* Header file for system calls opendir, readdir y closedir */
#include <linux/limits.h> /* To get PATH_MAX */

int main(int argc, char *argv[]){
	
	DIR *dir;

	if (argc < 2){ /*In case no parameter is passed*/
		
		char buffer[PATH_MAX];
		char *cwd = getcwd(buffer, sizeof(buffer));
		dir = opendir(cwd); /*To open the actual dir if no parameters passed*/

	}else{
		dir = opendir(argv[1]); /*To open the dir passed as a parameter*/
	}

	if (dir == NULL){ /*Returns -1 and prints an error if the directory was not found*/
		printf("Could not open directory\n");
		return -1;
	}

	struct dirent *dirp; /*Create a dirent type structure*/

	while ((dirp = readdir(dir)) != NULL){
		printf("%s\n",dirp->d_name); /*Prints and moves pointer*/
	}

	/*Closing directory*/

	closedir(dir);

	return 0;
}