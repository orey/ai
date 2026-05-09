/*
  mytools.c
  Author: rey.olivier@gmail.com
  Started: August 2025
 */
#ifndef _STDLIB_H
 #include <stdlib.h>
#endif
#ifndef _STDIO_H
  #include <stdio.h>
#endif
#ifndef _STDINT_H
  #include <stdint.h>
#endif
#ifndef _STDBOOL_H
  #include <stdbool.h>
#endif
#ifndef _WCHAR_H
  #include <wchar.h>
#endif
#ifndef _STRING_H
  #include <string.h>
#endif


#include "mytools.h"


/* The first byte of a UTF-8 character
 * indicates how many bytes are in
 * the character, so only check that
 */
int numberOfBytesInChar(unsigned char val) {
    if (val < 128) {
        return 1;
    } else if (val < 224) {
        return 2;
    } else if (val < 240) {
        return 3;
    } else {
        return 4;
    }
}

/* ====================================================== mybreakpoint*/
void wcmybreakpoint(wchar_t *str) {
  wprintf(L"%s\n", str);
  char response='a';
  printf("wcmybreakpoint: Do you want to continue? ['n' ends the treatment] ");
  scanf("%c", &response);
  if (response == 'n') {
    puts("Goodbye...");
    exit(0); // Exit gracefully
  }
  return;
}

/* ====================================================== mybreakpoint*/
void mybreakpoint(char *str) {
  printf("%s\n", str);
  char response='a';
  printf("mybreakpoint: Do you want to continue? ['n' ends the treatment] ");
  scanf("%c", &response);
  if (response == 'n') {
    puts("Goodbye...");
    exit(0); // Exit gracefully
  }
  else if (response == '\n') {
    return;
  }
  return;
}

/* ====================================================== is_utf8_continuation*/
bool is_utf8_continuation(uint8_t byte) {
    return (byte & 0xC0) == 0x80;
}

/* ====================================================== utf8_strlen*/
size_t utf8_strlen(const char *s) {
    size_t count = 0;
    while (*s) {
        uint8_t c = (uint8_t)*s;
        if ((c & 0x80) == 0) {
            // ASCII character (1 byte)
            s += 1;
        } else if ((c & 0xE0) == 0xC0) {
            // 2-byte character
            s += 2;
        } else if ((c & 0xF0) == 0xE0) {
            // 3-byte character
            s += 3;
        } else if ((c & 0xF8) == 0xF0) {
            // 4-byte character
            s += 4;
        }
        count++;
    }
    return count;
}

/* ====================================================== utf8_strlen*/
size_t utf8_offset(const char *s) {
    while (*s) {
        uint8_t c = (uint8_t)*s;
        if ((c & 0x80) == 0) {
            // ASCII character (1 byte)
            return 1;
        } else if ((c & 0xE0) == 0xC0) {
            // 2-byte character
            return 2;
        } else if ((c & 0xF0) == 0xE0) {
            // 3-byte character
            return 3;
        } else if ((c & 0xF8) == 0xF0) {
            // 4-byte character
            return 4;
        }
        else {
          printf("Unknown character: %d", c);
          return 0;
        }
    }
    return 0;
}

