# Makefile for Unix/Linux/macOS

CC = gcc
CFLAGS = -O2 -Wall -Wextra -std=c99
LDFLAGS = -lsqlite3
TARGET = xojodoc
SRC = src/main.c src/database.c src/display.c
OBJ = $(SRC:.c=.o)

# Platform detection
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
    # macOS
    LDFLAGS += -L/opt/homebrew/lib -I/opt/homebrew/include
endif

.PHONY: all clean install

all: $(TARGET)

$(TARGET): $(OBJ)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)
	strip $(TARGET)
	@echo ""
	@echo "Build successful! Binary: $(TARGET)"
	@ls -lh $(TARGET)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJ) $(TARGET)
	@echo "Cleaned build artifacts."

install: $(TARGET)
	install -m 755 $(TARGET) /usr/local/bin/
	@echo "Installed to /usr/local/bin/$(TARGET)"

# Static build (no external dependencies)
static: $(SRC)
	$(CC) $(CFLAGS) -o $(TARGET) $(SRC) -static -lsqlite3 -lpthread -ldl -lm
	strip $(TARGET)
	@echo ""
	@echo "Static build successful! Binary: $(TARGET)"
	@ls -lh $(TARGET)
