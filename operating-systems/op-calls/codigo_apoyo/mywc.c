//P1-SSOO-23/24

#include <stdio.h>  /* Header file for system call printf */
#include <unistd.h> /* Header file for system call open */
#include <fcntl.h>  /* For the flag O_RDONLY*/

#define BUFFER_SIZE 1 /*To read the file 1 by 1 byte*/

int main(int argc, char *argv[]){
	/*If less than two arguments (argv[0] -> program, argv[1] -> file to process) print an error y return -1*/
	if(argc < 2)
	{
		printf("Too few arguments\n");
		return -1;
	}

	/*We open the file*/

	int fd = open(argv[1], O_RDONLY); /*We open the file in read only mode*/
	if (fd == -1){                    /*Returns -1 and prints an error if file not found*/

		printf("File not found || Return -1\n");
		return -1;	
	}

	/*We read the file*/

	int i, bytes = 0, lines = 0, words = 0, found = 0;
	char buffer[BUFFER_SIZE], previous = ' ';
	
	while((i = read(fd, buffer, BUFFER_SIZE)) > 0){ /*Not 0 due to empty file*/
		
		/*We mark found as 1 when we find a letter, and count the word
		when found goes back to 0. When found is 0 it means it is a space, tab, 
		new line or carriage return*/

		found = 0;
		if (buffer[0] != ' ' && buffer[0] != '\t' && buffer[0] !='\n' && buffer[0] != 13){
			found = 1;
		}
		if (found == 0 && previous != ' ' && previous != '\t' && previous != '\n' && previous != 13){
			words++;
		}

		if (buffer[0] == '\n'){
			lines++;
		}
		previous = buffer[0];
		bytes++;
	}
	
	/*If the file only has one line with no \n, \t or blank spaces at the end*/

	if (previous != ' ' && previous != '\t' && previous != '\n')
	{
		words++;
	}
	
	int close(int fd); 	/*We close the file*/
	printf("%d %d %d %s\n", lines, words, bytes, argv[1]); /*We print the output*/
	return 0;
}