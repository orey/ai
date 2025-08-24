/*
  mytools.c
  Author: rey.olivier@gmail.com
  Started: August 2025
 */

#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>


#include "mytools.h"


/* This function tales in charge multi-byte chars */
bool charEquals(char* a, char* b){
  //debug
  /*char trace[100];
  sprintf(trace, "%s - %s", a, b);
  mybreakpoint(trace);*/
  //end debug
  int na = numberOfBytesInChar(a);
  int nb = numberOfBytesInChar(b);
  if (na != nb) return false;
  switch(na){
  case 1:
    //ascii 7bits chars
    if (a[0] == b[0]) return true;
    else return false;
  case 2:
    if ((a[0] == b[0])
        && (a[1] == b[1])) return true;
    else return false;
  case 3:
    if ((a[0] == b[0])
        && (a[1] == b[1])
        && (a[2] == b[2]))
      return true;
    else return false;
  case 4:
    if ((a[0] == b[0])
        && (a[1] == b[1])
        && (a[2] == b[2])
        && (a[3] == b[3]))
      return true;
    else return false;
  default:
    perror("This case should never happen.");
    return false;
  }
}

/* The first byte of a UTF-8 character
 * indicates how many bytes are in
 * the character, so only check that
 */
int numberOfBytesInChar(char * c) {
  unsigned char val = c[0];
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

