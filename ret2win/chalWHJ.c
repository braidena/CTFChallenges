#include <stdio.h>
#include <string.h>

void win() {
    puts("flag{win}");
}

void vuln() {
    char buf[64];
    
    fgets(buf, 128, stdin);
    
}   
int main() {
    vuln();
    return 0;
}