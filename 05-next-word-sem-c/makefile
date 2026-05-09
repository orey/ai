# Cross-platform Makefile for Linux and Cygwin
# Uses GNU Make >= 4.2

CC      := gcc
CFLAGS  := -Wall -Wextra
OBJ     := main.o mytools.o mysymbols.o

# Different targets for release and debug
TARGET_RELEASE := program.x
TARGET_DEBUG   := program_debug.x

# Default target builds release
all: release

# Release build (optimized)
release: CFLAGS += -O2
release: $(OBJ)
	$(CC) $(CFLAGS) -o $(TARGET_RELEASE) $^

# Debug build (debug symbols, no optimization)
debug: CFLAGS += -g -O0
debug: $(OBJ)
	$(CC) $(CFLAGS) -o $(TARGET_DEBUG) $^

# Compile .c into .o
%.o: %.c mytools.h mysymbols.h
	$(CC) $(CFLAGS) -c $< -o $@

# Clean build files
clean:
	rm -f $(OBJ) $(TARGET_RELEASE) $(TARGET_DEBUG)

.PHONY: all release debug clean

