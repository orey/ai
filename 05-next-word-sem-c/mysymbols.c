/*
  mysymbols.c
  Author: rey.olivier@gmail.com
  Started: August 2025
 */

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "mytools.h"
#include "mysymbols.h"

/* ====================================================== iniSymbols */
/* factory of Symbols */
Symbols * initSymbols(){
  Symbols * symbs = (Symbols *) malloc(sizeof(Symbols));
  symbs->len = 0;
  return symbs;
}

/* ====================================================== iniSymbols */
void printSymbols(Symbols * symbs){
  printf("%d symbols in the array of symbols\n[", symbs->len);
  for (int i=0;i<(symbs->len);i++){
    printf("'%s', ",symbs->symbols[i]);
  }
  printf("]\n");
}

/* ====================================================== addSymbolToSymbols*/
void addSymbolToSymbols(Symbols * symbs, char * newsymb) {
  for (int i=0;i<(symbs->len);i++){
    if (charEquals(symbs->symbols[i],newsymb)){
      //we have it already
      return;
    }
  }
  // it is a new symbol
  strcpy(symbs->symbols[symbs->len], newsymb);
  (symbs->len)++;
  //printf("New symbol: '%s' --- Number of symbols: %d\n",newsymb,symbs->len);
}
