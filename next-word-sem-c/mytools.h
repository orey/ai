/*
  mytools.h
  Author: rey.olivier@gmail.com
  Started: August 2025
 */

#include <stdint.h>
#include <stdbool.h>

#ifndef _MYTOOLS_H
#define _MYTOOLS_H

void mybreakpoint(char * str);

int numberOfBytesInChar(char * c);
bool charEquals(char* a, char* b);

bool is_utf8_continuation(uint8_t byte);

size_t utf8_strlen(const char *s);

size_t utf8_offset(const char *s);

  
#endif //_MYTOOLS_H

