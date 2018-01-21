# Simple MicroProcessor Architecture
SMPA CPU v0.1 - Open Source 8bit CPU concept by Nikita Lindmann  
https://sw.ramiil.in/?page=loca_russian  

### REGISTERS
Registers 1-6 is common use registers AR-FR  
7-12'th registers are reserved  
13 and 14'th registers (IPTR and SEGR) are used for addressation  
15 is FLAGS register  
Zero register is special register for each function's result(LASTR)  

### ADDRESSATION
Full byte address is SEGR*255+IPTR, limited by 65536 bytes or 64 kbyte.  
First 6400 bytes reserved for BIOS and Memory mapped IO(means it's readonly).  

### OPCODES
Register-register commands:
```
0000'0000 0000'0000
\_______/ \__/ \__/
 Opcode   Registers
```

Valie commands:
```
0000'0000 0000'0000
\_______/ \_______/
 Opcode     Value
```

#### Nothing
0x00 - nop - *Do nothing*  

**Memory and register operations**  
0x01 - rmem Reg, Reg - *Load data from memory at Reg:Reg(page:offset) to LASTR*  
0x02 - wmem Reg, Reg - *Store data from LASTR to memory at Reg:Reg(page:offset)*  
0x03 - mv Reg Reg - *Copy data from first register to second, LASTR not changes*  
0x04 - rev Reg - *Copy data from register to LASTR*  

#### Math and logic
0x05 - add Reg, Reg - *Add integer value from first register to second*  
0x06 - or Reg, Reg - *Bit OR logic function*  
0x07 - and Reg, Reg - *Bit AND logic function*  
0x08 - not Reg - *Logical inversion*  

#### Branching
0x09 - jmp Reg, Reg - *Jump to Reg:Reg(page:offset)*  
0x0A - eq Reg, Reg - *If data in both registers is equal, next command will be passed*  
0x0B - less Reg, Reg  
0x0C - more Reg, Reg  
0x0D - leq Reg, Reg  
0x0E - meq Reg, Reg  
0x0F - neq Reg, Reg  

#### Direct data load
0x10 - setAR Value - *Load Value to register AR*  
0x11 - setBR Value  
0x12 - setCR Value  
0x13 - setDR Value  
0x14 - setER Value  
0x15 - setFR Value  
0x16 - setFLAGR Value  

#### Stack operations
0x17 - ls Reg - *Load data from top of stack to LASTR*  
0x18 - ss Reg - *Save data from reg to top of stack*  

#### Interruptions
0x19 - int Value - *Generate interruption*  

### INTERRUPTIONS LIST
00 Does nothing
01 Halts the cpu
02 Send single character from LASTR onto screen.  
03 Read singe character from buffer to LASTR.  