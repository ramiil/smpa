import struct

MaxMemorySize = 65536
UserCodeStartPage = 6400
AR = 0
BR = 1
CR = 2
DR = 3
ER = 4
FR = 5

IPTR = 6
SEGR = 7

FLAGR = 14
LASTR = 15

class smpaCPU:
        ramdata = [b'\x00'] * MaxMemorySize
        registers = [0] * 16
        haltSignal = False

        def init(self):
                for i in range(1, MaxMemorySize):
                        self.ramdata[i] = 0x00
                ramfile = open('ramfile.bin', 'rb')
                writePtr = UserCodeStartPage
                while (True):
                        self.ramdata[writePtr] = ramfile.read(1)
                        if not self.ramdata[writePtr]:
                                break
                        writePtr+=1
        
        def decodeReg(self, regfile):
                return (regfile>>4, regfile&0xF)

        def cpuTick(self, fx, ops):
                print('Tick', self.registers[IPTR])
                print(ord(fx), ' ', ord(ops))
                regA, regB = self.decodeReg(ord(ops))
                if (fx==b'\x00'):
                        0+0 # Do nothing
                        print('No operation')
                        print(self.registers)
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
                        self.registers[IPTR] = 6400+(self.registers[regA]*self.registers[regB])
                        print('LOL IM DA BUNNY')

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
                        self.registers[AR] = ord(ops)
                if (fx==b'\x11'):
                        self.registers[BR] = ord(ops)
                if (fx==b'\x12'):
                        self.registers[CR] = ord(ops)
                if (fx==b'\x13'):
                        self.registers[DR] = ord(ops)
                if (fx==b'\x14'):
                        self.registers[ER] = ord(ops)
                if (fx==b'\x15'):
                        self.registers[FR] = ord(ops)
                if (fx==b'\x16'):
                        self.registers[FLAGR] = ord(ops)
                if (fx==b'\x17'):
                        self.registers[LASTR] = ord(ops)
                if (fx==b'\x18'):
                        self.registers[SEGR] = ord(ops)
                if (fx==b'\x19'):
                        self.registers[IPTR] = ord(ops)

                if (fx==b'\x1A'):
                        0+0 # It will be "Load from Stack"
                if (fx==b'\x1B'):
                        0+0 # It will be "Save to Stack"

                if (fx==b'\x1C'):
                        0+0 # It will be "Generate interrupt"
                if (fx==b'\x1D'):
                        self.haltSignal = True # Makes CPU stop
                if (fx==b'\x1E'):
                        0+0 # Do nothing
                        
def main():
        cpu = smpaCPU()
        cpu.registers[IPTR] = 6400
        cpu.init()
        while (not cpu.haltSignal):
                fx = cpu.ramdata[cpu.registers[IPTR]]
                ops = cpu.ramdata[cpu.registers[IPTR]+1]
                cpu.registers[LASTR] = cpu.cpuTick(fx, ops)
                cpu.registers[IPTR] += 2

main()