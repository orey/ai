/*
  mytools.h
  Author: rey.olivier@gmail.com
  Started: August 2025
 */
#ifndef _STDINT_H
  #include <stdint.h>
#endif
#ifndef _STDBOOL_H
  #include <stdbool.h>
#endif
#ifndef _WCHAR_H
  #include <wchar.h>
#endif

#ifndef _MYTOOLS_H
#define _MYTOOLS_H

void mybreakpoint(char * str);
void wcmybreakpoint(wchar_t *str);


int numberOfBytesInChar(unsigned char val);

bool is_utf8_continuation(uint8_t byte);

size_t utf8_strlen(const char *s);

size_t utf8_offset(const char *s);

  
#endif //_MYTOOLS_H

