/*
  mysymbols.h
  Author: rey.olivier@gmail.com
  Started: August 2025
 */

#ifndef _MYSYMBOLS_H
#define _MYSYMBOLS_H

/* ====================================================== Symbols struct */
typedef struct the_symbols {
  char symbols[200][4]; //200 chars of 4 bytes each max
  int len;
} Symbols;

Symbols * initSymbols();

void printSymbols(Symbols * symbs);

void addSymbolToSymbols(Symbols * symbs, char * newsymb);

#endif //_MYSYMBOLS_H
