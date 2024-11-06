//P1-SSOO-23/24

#include <stdio.h>	  /* Header file for system call printf */
#include <unistd.h>	  /* Header file for system call gtcwd */
#include <dirent.h>   /* Header file for system calls opendir, readdir y closedir */
#include <string.h>   /* To use strcmp*/

int main(int argc, char *argv[]){
	/* If less than three arguments (argv[0] -> program, argv[1] -> directory to search, argv[2] -> file to find) print an error y return -1 */
	if(argc < 3)
	{
		printf("Too few arguments\n");
		return -1;
	}

	/*Configure the directory*/

	DIR *dir = opendir(argv[1]);

	if (dir == NULL){ /*Returns -1 and prints an error if the directory was not found*/
		printf("Could not open directory\n");
		return -1;
	}

	int found = 1;
	struct dirent *dirp;
	
	/*We loop until the pointer is NULL or we have found the file wanted*/
	while ((dirp = readdir(dir)) != NULL && found != 0){
		if (strcmp(dirp->d_name, argv[2]) == 0){   /*If 0, both strings are equal*/		
			printf("File %s is in directory %s\n", argv[2], argv[1]);
			found = 0;
		} 
	}

	/*If the file is not found, we print a message*/
	if (found != 0){
		printf("File %s is not in directory %s\n", argv[2], argv[1]);
	}

	closedir(dir); /*We close the directory*/

	return 0;
}