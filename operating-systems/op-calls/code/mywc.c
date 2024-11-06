//P1-SSOO-23/24

#include <stdio.h> 
#include <unistd.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/mman.h>

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

	int i, bytes = 0, lines = 0, words = 0;
	char buffer[BUFFER_SIZE], previous = ' ';
	
	while((i = read(fd, buffer, BUFFER_SIZE)) > 0){ /*Not 0 due to empty file*/

		//printf("%d\n", (int)buffer[0]); 
		/*Espacio == 32
		Tab == 9
		Intro == 10*/

		if((buffer[0] == ' ' || buffer[0] == '\t')
		&& (previous != ' ' && previous != '\t' && previous !=  '\n')){  /*Every time we find a blanc space or a tab, we have read a word*/
			words++;
		}

		if((buffer[0] == 13) /*RETORNO DE CARRO*/
		&& (previous != ' ' && previous != '\t' && previous != '\n')){ /*When we find a "\n", we add a word and a line*/
			lines++;
			words++;

		}else if (buffer[0] == 13){
			lines++;
		}
		

		// if((buffer[0] == '\n') 
		// && (previous != ' ' && previous != '\t' && previous != '\n')){ /*When we find a "\n", we add a word and a line*/
		// 	lines++;
		// 	words++;
		// 	// printf("Buffer %c", buffer[0]);
		// 	// printf("Previous %c", previous);
		// }

		previous = buffer[0]; /*To keep the last element read*/
		bytes++;
	}

	/*This helps in order to add a word in case a file does not end in " ", "\n" or "\t".
	If a file does not end in any of this three characters and the number of bytes != 0, we add a word.
	In case the file does end in some of the characters, the word would have already be counted in 
	the loop above and we skip*/

	if (previous != ' ' && previous != '\t' && previous != '\n' && bytes != 0)
	{
		words++;
	}

	int close(int fd); 	/*We close the file*/
	printf("%d %d %d %s\n", lines, words, bytes, argv[1]); /*We print the output*/
	return 0;
}