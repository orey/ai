/* This may look like nonsense, but really is -*- mode: C -*- */

#ifndef _STDLIB_H
  #include <stdlib.h>
#endif
#ifndef _STDIO_H
  #include <stdio.h>
#endif
#ifndef _STDBOOL_H
  #include <stdbool.h>
#endif
#ifndef _CTYPE_H
  #include <ctype.h>
#endif
#ifndef _WCHAR_H
  #include <wchar.h>
#endif
#ifndef _STRING_H
  #include <string.h>
#endif


#ifndef _MYTOOLS_H
  #include "mytools.h"
#endif




size_t parseFile2(char * filename) {
  FILE *fptr = fopen(filename, "rb");
  if (fptr == NULL) {
    perror("Error opening file");
    return 1;
  }
  char c[5] = {'\0'};
  char word[50] = "";
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
    // the c character is captured
    /*printf("%d\n",(unsigned char) c[0]);
      mybreakpoint(c);*/
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
    if (count == 100) {
      puts("End of test");
      exit(0);
    } 
  } //end of while
  return count;
}



/* ====================================================== ParseFile*/
size_t parseFile(char* filename) {
  wchar_t c;
  wchar_t word[100]; //longest word ever
  
  FILE *fptr = fopen(filename, "rb"); //read bytes

  int count = 0;
  const wchar_t space = L' ';
  mybreakpoint(filename);

  wchar_t a = L'é';
  wcmybreakpoint(&a);

  wcscpy(word,L"");
  while ((c =fgetwc(fptr)) != EOF ) {
    wcmybreakpoint(&c);
    wcmybreakpoint(word);
    if (c == space) {
      puts("titi");
      //new word to print
      wprintf(L"%s |", word);
      wcscpy(word,L"");
      count++;
    }
    else {
      puts("toto");
      wcscat(word, &c);
      wcmybreakpoint(word);
      puts("titi");
    }
    fptr += sizeof(c);
    if (count > 1000) {
      puts("Fin du test");
      exit(0);
    }
    puts("tutu");
  }
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
int main(int argc, [[maybe_unused]] char* argv[argc+1]) {
  printf("\nSize of int: %lu\n", sizeof(int));
  printf("Size of size_t: %lu\n", sizeof(size_t));

  // bool result = parseFile("segond-clean.txt");
  //printf("%b", result);
  readUtf8File("segond-clean.txt");
  puts("=============================================");
  parseFile2("segond-clean.txt");
    
  return EXIT_SUCCESS;
}
