#==========================================================================
#
#   The PyRISC Project
#
#   SNURISC5: A 5-stage Pipelined RISC-V ISA Simulator
#
#   Classes for hardware components: RegisterFile, Memory, Adder, etc.
#
#   Jin-Soo Kim
#   Systems Software and Architecture Laboratory
#   Seoul National University
#   http://csl.snu.ac.kr
#
#==========================================================================


from consts import *
from isa import *


#--------------------------------------------------------------------------
#   Constants
#--------------------------------------------------------------------------

# Symbolic register names
rname =  [ 
            'zero', 'ra',  'sp',  'gp',  'tp',  't0',  't1',  't2',
            's0',   's1',  'a0',  'a1',  'a2',  'a3',  'a4',  'a5',
            'a6',   'a7',  's2',  's3',  's4',  's5',  's6',  's7',
            's8',   's9',  's10', 's11', 't3',  't4',  't5',  't6' 
        ]


#--------------------------------------------------------------------------
#   RegisterFile: models 32-bit RISC-V register file
#--------------------------------------------------------------------------

class RegisterFile(object):

    def __init__(self):
        self.reg = WORD([0] * NUM_REGS)

    def read(self, regno):

        if regno == 0:
            return 0
        elif regno > 0 and regno < NUM_REGS:
            return self.reg[regno]
        else:
            raise ValueError

    def write(self, regno, value):

        if regno == 0:
            return
        elif regno > 0 and regno < NUM_REGS:
            self.reg[regno] = WORD(value)
        else:
            raise ValueError

    def dump(self, columns = 4):

        print("Registers")
        print("=" * 9)
        for c in range (0, NUM_REGS, columns):
            str = ""
            for r in range (c, min(NUM_REGS, c + columns)):
                name = rname[r]
                val = self.reg[r]
                str += "%-11s0x%08x    " % ("%s ($%d):" % (name, r), val)
            print(str)

        print("")


#--------------------------------------------------------------------------
#   Register: models a single 32-bit register
#--------------------------------------------------------------------------

class Register(object):

    def __init__(self, initval = 0):
        self.r = WORD(initval)

    def read(self):
        return self.r

    def write(self, val):
        self.r = WORD(val)


#--------------------------------------------------------------------------
#   Memory: models a memory
#--------------------------------------------------------------------------

class Memory(object):

    def __init__(self, mem_start, mem_size, word_size):
        self.word_size  = word_size
        self.mem_start  = mem_start
        self.mem_end    = mem_start + mem_size
        self.mem        = bytearray(mem_size)

    def access(self, valid, addr, data, fcn):
        if (not valid):
            res = ( WORD(0), True )
        elif (addr < self.mem_start) or (addr >= self.mem_end) or \
            addr % self.word_size != 0:
            res = ( WORD(0) , False )
        elif fcn == M_XRD:
            offset = addr - self.mem_start
            val = int.from_bytes(self.mem[offset:offset+self.word_size], 'little')
            res = ( WORD(val), True )
        elif fcn == M_XWR:
            data = int(data)
            offset = addr - self.mem_start
            self.mem[offset:offset+self.word_size] = data.to_bytes(self.word_size, 'little')
            res = ( WORD(0), True )
        else:
            res = ( WORD(0), False )

        return res

    def copy_to(self, addr, data):
        if (addr < self.mem_start) or (addr + len(data) > self.mem_end):
            raise Exception(f"Cannot copy data into memory: invalid address {addr:08x} - {addr+len(data):08x}")

        offset = addr - self.mem_start
        self.mem[offset:offset+len(data)] = data

    def copy_from(self, addr, nbytes):
        if (addr < self.mem_start) or (addr + nbytes > self.mem_end):
            raise Exception(f"Cannot copy data from memory: invalid address {addr:08x} - {addr+len(data):08x}")

        data = bytearray(nbytes)
        offset = addr - self.mem_start
        data[0:nbytes] = self.mem[offset:offset+nbytes]

        return data

    def dump(self, skipzero = False):

        print("Memory 0x%08x - 0x%08x" % (self.mem_start, self.mem_end - 1))
        print("=" * 30)
        skipz = False
        printsz = True

        adr_range=range(self.mem_start, self.mem_end, self.word_size);
        for a in adr_range:
            val, status = self.access(True, a, 0, M_XRD)
            if not status:
                continue
            if (not skipzero) or (not skipz) or (val != 0) or (a == adr_range[-1]):
                skipz = val == 0
                printsz = True
                print("0x%08x: " % a, ' '.join("%02x" % ((val >> i) & 0xff) for i in [0, 8, 16, 24]), " (0x%08x)" % val)
            elif printsz:
                printsz = False
                print("             ...")

        print("")


#--------------------------------------------------------------------------
#   ALU: models an ALU
#--------------------------------------------------------------------------

class ALU(object):

    def __init__(self):
        pass

    def op(self, alufun, alu1, alu2):

        np.seterr(all='ignore')
        if alufun == ALU_ADD:
            output = WORD(alu1 + alu2)
        elif alufun == ALU_SUB:
            output = WORD(alu1 - alu2)
        elif alufun == ALU_AND:
            output = WORD(alu1 & alu2)
        elif alufun == ALU_OR:
            output = WORD(alu1 | alu2)
        elif alufun == ALU_XOR:
            output = WORD(alu1 ^ alu2)
        elif alufun == ALU_SLT:
            output = WORD(1) if SWORD(alu1) < SWORD(alu2) else WORD(0)
        elif alufun == ALU_SLTU:
            output = WORD(1) if alu1 < alu2 else WORD(0)
        elif alufun == ALU_SLL:
            output = WORD(alu1 << (alu2 & 0x1f))
        elif alufun == ALU_SRA:
            output = WORD(SWORD(alu1) >> (alu2 & 0x1f))
        elif alufun == ALU_SRL:
            output = alu1 >> (alu2 & 0x1f)
        elif alufun == ALU_COPY1:
            output = alu1
        elif alufun == ALU_COPY2:
            output = alu2
        elif alufun == ALU_SEQ:
            output = WORD(1) if (alu1 == alu2) else WORD(0)
        elif alufun == ALU_MUL:
            output = WORD(alu1 * alu2)
        elif alufun == ALU_SVUNPACK: # when unpack, make alu1 to vector data
            output = WORD(((alu1 & 0xff0000) << 4) | ((alu1 & 0xff00) << 2) | (alu1 & 0xff))
        elif alufun == ALU_SVPACK: # when pack, make alu1 to raw data
            SAT = lambda c: c if WORD(c) <= 0xff else 0xff # SAT function
            output = WORD((alu2<<24) | SAT((alu1>>20)&0x3ff)<<16 | SAT((alu1>>10)&0x3ff)<<8 | SAT(alu1&0x3ff))
        elif alufun == ALU_SVBRDCST: # when broadcast, make vector using alu's 8bit repeatedly 
            output = WORD(((alu1<<20)&0x3ff00000) | ((alu1<<10)&0xffc00) | (alu1&0x3ff))
        elif alufun == ALU_SVADDI: # when addi, add alu1 vector to immediate vector
            output = WORD(WORD(WORD(alu1+WORD(alu2<<20))&0x3ff00000) | WORD(WORD(alu1+WORD(alu2<<10))&0xffc00) | WORD(WORD(alu1+alu2)&0x3ff))
        elif alufun == ALU_SVADD: # when add, add alu1 vector to alu2 vector 
            output = WORD((((alu1&0x3ff00000)+(alu2&0x3ff00000))&0x3ff00000) | (((alu1&0xffc00)+(alu2&0xffc00))&0xffc00) | (((alu1&0x3ff)+(alu2&0x3ff))&0x3ff))
        elif alufun == ALU_SVSUB: # when sub, sub alu2 vector from alu1 vector
            output = WORD(WORD(WORD(WORD(alu1&0x3ff00000)-WORD(alu2&0x3ff00000))&0x3ff00000) | WORD(WORD(WORD(alu1&0xffc00)-WORD(alu2&0xffc00))&0xffc00) | WORD(WORD(WORD(alu1&0x3ff)-WORD(alu2&0x3ff))&0x3ff))
        elif alufun == ALU_SVMUL: # when mul, multiply alu1 vector to alu2 vector
            ROUND = lambda c: (c >> 8) + 0 if (c&0xff) < 0x80 else (c >> 8) + 1 # ROUND function
            output = WORD((ROUND(((alu1 >> 20) & 0x3FF) * ((alu2 >> 20) & 0x3FF))) << 20 | (ROUND(((alu1 >> 10) & 0x3FF) * ((alu2 >> 10) & 0x3FF))) << 10 | ROUND((alu1 & 0x3FF) * (alu2 & 0x3FF)))
        else:
            output = WORD(0)

        return output



#--------------------------------------------------------------------------
#   Adder: models a simple 32-bit adder
#--------------------------------------------------------------------------

class Adder(object):

    def __init__(self):
        pass

    def op(self, operand1, operand2 = 4):
        np.seterr(all='ignore')
        return WORD(operand1 + operand2)


