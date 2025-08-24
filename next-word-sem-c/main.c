/*
  AI
  OR rey.olivier@gmail.com
  August 2025
 */

#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <ctype.h>
#include <string.h>

#include "mytools.h"
#include "mysymbols.h"






/* ====================================================== parseFile*/
size_t parseFile(char * filename, int threshold) {
  //init the symbol table
  Symbols* symbs = initSymbols();
  //manage the file
  FILE *fptr = fopen(filename, "rb");
  if (fptr == NULL) {
    perror("Error opening file");
    return 1;
  }
  char c[5] = {0};
  char word[50] = {0};
  int count = 0;
  //((bytesRead = fread(buffer, 1, sizeof(buffer) - 1, filePointer)) > 0){
  int bytesRead = 0;
  while ((bytesRead = fread(c, 1, 1, fptr)) > 0) {
    unsigned char val = c[0];
    if (val < 128) {
      c[1] = '\0';
    }
    else if (val < 224) {
      // 2 bytes
      fread(&c[1], 1, 1, fptr);
      c[2] = '\0';
    }
    else if (val < 240) {
      // 3 bytes
      fread(&c[1], 1, 2, fptr);
      c[3] = '\0';
    }
    else {
      fread(&c[1], 1, 3, fptr);
      c[4] = '\0';
      }
    // the 'c' character is captured
    /*printf(">>> The char captured is\n");
    mybreakpoint(c);
    puts("calling addSymbolToSymbols <<<");*/
    addSymbolToSymbols(symbs,c);
    if (c[0] == ' ') {
      //word is a complete word
      printf("%s | ", word);
      count++;
      word[0] = '\0';
    }
    else {
      strcat(word, c);
    }
    c[0] = '\0';
    // A enlever
    if (threshold != 0) {
      if (count == threshold) {
        puts("End of test");
        printSymbols(symbs);
        return count;
      }
    }
  } //end of while
  printSymbols(symbs);
  return count;
}


/* ====================================================== readUtf8File*/
int readUtf8File(char * filename) {
  FILE *file = fopen(filename, "rb"); // "rb" for binary mode
  if (!file) {
    perror("Failed to open file");
    return 1;
  }

  char buffer[1024];
  size_t bytes_read = fread(buffer, 1, sizeof(buffer), file);
  buffer[bytes_read] = '\0'; // Null-terminate for safety
  printf("Read: %s\n", buffer);

  fclose(file);
  return 0;
}





/* ====================================================== MAIN*/
int main(int argc, char** argv) {
  decodeArguments(argc, argv);
  
  printf("\nSize of int: %lu\n", sizeof(int));
  printf("Size of size_t: %lu\n", sizeof(size_t));

  readUtf8File("segond-clean.txt");
  puts("=============================================");

  timer * tim = startTimer("01234567890123456789012345678901", true);
  //parseFile("segond-clean.txt", 1000);
  parseFile("segond-clean.txt", 0);
  stopTimer(tim, true);
  puts("END");



    
    
  return 0;
}
