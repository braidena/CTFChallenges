CC = gcc 
CFLAGS = -g -O0 -fno-stack-protector -no-pie
TARGET = chalWHJ

all: $(TARGET)

$(TARGET): chalWHJ.c
	$(CC) $(CFLAGS) -o $(TARGET) chalWHJ.c

clean:
	rm -f $(TARGET)