import struct

BitDepth=16
MaxMemorySize = 2**BitDepth
UserCodeStartPage = 6400

AR = 1
BR = 2
CR = 3
DR = 4
ER = 5
FR = 6

IPTR = 13
SEGR = 14
FLAGR = 15

LASTR = 0
  
class smpaCPU:
  ramdata = [b'\x00'] * MaxMemorySize
  registers = [0] * 16
  haltSignal = False
  
  def interrupt(self, intID):
    if (intID==0):
      pass # Do nothing
    if (intID==1):
      # Halt
      self.haltSignal = True
    if (intID==2):
      print(chr(self.registers[FR]), end=" ")

  def init(self):
    for i in range(1, MaxMemorySize):
      self.ramdata[i] = 0x00
    bootloader = open('bootloader.bin', 'rb')
    ramfile = open('ramfile.bin', 'rb')

    writePtr = 0
    while (True):
      self.ramdata[writePtr] = bootloader.read(1)
      if not self.ramdata[writePtr]:
        break
      writePtr+=1

    writePtr = UserCodeStartPage
    while (True):
      self.ramdata[writePtr] = ramfile.read(1)
      if not self.ramdata[writePtr]:
        break
      writePtr+=1

  def setRegValue(self, register, value):
    if not (register==IPTR or register==SEGR):
      self.registers[register] = value
    else:
      self.interrupt(1)
    
  def getRegValue(self, register):
    return self.registers[register]
    
  def decodeReg(self, regfile):
    return (regfile>>4, regfile&0xF)
    
  def readMemory(self, segment, offset):
    return self.ramdata[(segment*255)+offset]
    
  def writeMemory(segment, offset, data):
    pass
    # self.ramdata[(segment*255)+offset] == data
    
  def tick(self):
    # Wanna some real Hindi code? Got it!
    realaddr = (self.registers[SEGR]*255)+self.registers[IPTR]
    realaddr += 2
    self.registers[SEGR] = realaddr // 255
    self.registers[IPTR] = realaddr % 255

  def runit(self, fx, ops):
    regA, regB = self.decodeReg(ord(ops))
    
    print('Command: ', fx, ' Data: ', ops)
    
    if (fx==b'\x00'):
      pass # RESERVED
    if (fx==b'\x01'):
      return self.ramdata[self.registers[regA]*self.registers[regB]]
    if (fx==b'\x02'):
      self.ramdata[self.registers[regA]*self.registers[regB]] = self.registers[LASTR]
    if (fx==b'\x03'):
      self.registers[regA] = self.registers[regB]
    if (fx==b'\x04'):
      self.registers[regA] = -self.registers[regB]

    if (fx==b'\x05'):
      return self.registers[regA]+self.registers[regB]
    if (fx==b'\x06'):
      return self.registers[regA]|self.registers[regB]
    if (fx==b'\x07'):
      return self.registers[regA]&self.registers[regB]
    if (fx==b'\x08'):
      return not(self.registers[regA])

    if (fx==b'\x09'):
      # Should be redone
      self.registers[SEGR] = self.registers[regA]
      self.registers[IPTR] = self.registers[regB]
      input()

    if (fx==b'\x0A'):
      if (self.registers[regA]==self.registers[regB]):
        self.registers[IPTR] += 2
    if (fx==b'\x0B'):
      if (self.registers[regA]<self.registers[regB]): # Less
        self.registers[IPTR] += 2
    if (fx==b'\x0C'):
      if (self.registers[regA]>self.registers[regB]): # More
        self.registers[IPTR] += 2
    if (fx==b'\x0D'):
      if (self.registers[regA]<=self.registers[regB]):
        self.registers[IPTR] += 2
    if (fx==b'\x0E'):
      if (self.registers[regA]>=self.registers[regB]):
        self.registers[IPTR] += 2
    if (fx==b'\x0F'):
      if (self.registers[regA]!=self.registers[regB]):
        self.registers[IPTR] += 2

    if (fx==b'\x10'):
      self.setRegValue(AR, ord(ops))
    if (fx==b'\x11'):
      self.setRegValue(BR, ord(ops))
    if (fx==b'\x12'):
      self.setRegValue(CR, ord(ops))
    if (fx==b'\x13'):
      self.setRegValue(DR, ord(ops))
    if (fx==b'\x14'):
      self.setRegValue(ER, ord(ops))
    if (fx==b'\x15'):
      self.setRegValue(FR, ord(ops))
    if (fx==b'\x16'):
      self.setRegValue(FLAGR, ord(ops))

    if (fx==b'\x17'):
      pass # It will be "Load from Stack"
    if (fx==b'\x18'):
      pass # It will be "Save to Stack"

    if (fx==b'\x19'):
      self.interrupt(self.getRegValue(regA))
    if (fx==b'\xFF'):
      print("DUMP REGS ", self.registers)
      
def main():
  cpu = smpaCPU()
  cpu.init()
  while (not cpu.haltSignal):
    instruction = cpu.readMemory(cpu.registers[SEGR], cpu.registers[IPTR])
    data = cpu.readMemory(cpu.registers[SEGR], cpu.registers[IPTR]+1)
    cpu.registers[LASTR] = cpu.runit(instruction, data)
    cpu.tick()

main()
