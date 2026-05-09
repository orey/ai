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

#ifndef _MYTOOLS_H
  #include "mytools.h"
#endif


bool parseFile(char* filename) {
  bool found_word = false;
  char c;
  FILE *fptr = fopen(filename, "r");
  while ((c =fgetc(fptr)) != EOF ) {
    if (!isalpha(c))
      {
        if (found_word) {
          putchar('\n');
          found_word = 0;
        }
      }
    else {
      found_word = true;
      c = tolower(c);
      putchar(c);
      char *temp = "-";
      sprintf(temp, "%c", c);
      //mybreakpoint(temp);
    }
  }
  return true;
}




/* ====================================================== MAIN*/
int main(int argc, [[maybe_unused]] char* argv[argc+1]) {
  printf("\nSize of int: %lu\n", sizeof(int));
  printf("Size of size_t: %lu\n", sizeof(size_t));

  bool result = parseFile("segond-clean.txt");
  printf("%b", result);
  
  return EXIT_SUCCESS;
}
