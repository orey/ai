/*
  mytools.h
  Author: rey.olivier@gmail.com
  Started: August 2025
 */

#include <stdint.h>
#include <stdbool.h>
#include <time.h>

#ifndef _MYTOOLS_H
#define _MYTOOLS_H


typedef unsigned char uchar;


/* ====================================================== timer type */
typedef struct timer_t {
  char name[30];
  time_t start;
  time_t stop;
  double dif;
} timer;


timer * startTimer(char * name, bool verbose);
long stopTimer(timer * thetimer, bool verbose);

void mystrncpy(char * target, char * source, int maxlen);
void decodeArguments(int argc, char ** argv);
void mybreakpoint(char * str);

int numberOfBytesInChar(char * c);
bool charEquals(char* a, char* b);

bool is_utf8_continuation(uint8_t byte);

size_t utf8_strlen(const char *s);

size_t utf8_offset(const char *s);

  
#endif //_MYTOOLS_H

