# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 23:09:51 2019

@author: redne

***************************
******INTCODE MACHINE******
***************************
Turing-esq machine for running Intcode for Advent of Code 2019 challenges

Operation:
    Intcode is defined as a set of comma-separated integers that is the machine's 
    program and initial Memory state. An index in memory is called an Address.
    Instructions are composed of one Opcode and any number of Parameters
    (including no parameters). The address of the machine's current instruction
    is called the Instruction Pointer, and starts at 0 at the beginning of operation.
    After completing the instruction, the instruction pointer is incremented by
    the size of the executed function (including opcode and params) to move it
    to the beginning of the next instruction.
    
    For the purposes of the day 2 challenges, the program has 2 inputs, called
    the Noun and the Verb. These two values specify the initial values of the
    addresses 1 and 2 to be the noun and verb respectively.
    
Function Set:
    ## - params - functionality description
    00 - _      - not defined
    01 - _ABC   - adds values at A and B and stores in C
    02 - _ABC   - multiplies values at A and B and stores in C
    03 - _      - not defined
    ...
    98 - _      - not defined
    99 - _      - terminate program

"""

outputs = []

def safe_list_get (l, idx, default):
  try:
    return l[idx]
  except IndexError:
    return default

#   Intcode interpreter, modify as needed to suit challenge purpose
def runProgram(prgm):
    mem = [int(i) for i in prgm.split(",")]
    #mem[1] = int(noun)
    #mem[2] = int(verb)
    
    ip = 0      # instruction pointer
    opCount = 0 # variable to keep track of instructions run
    while True:
        opcode = str(mem[ip])
        instr = int(opcode[-2:])
        modes = opcode[:-2]
        modes = modes[::-1] # reverse
        print("IP:", ip, "instr:", instr, "modes:", modes, "(raw)=", opcode)
        opCount += 1
        if   (instr == 1):     # Add operation
            opsize = 4
            addr1 = mem[ip+1]
            addr2 = mem[ip+2]
            addr3 = mem[ip+3]
            print("     ",addr1,addr2,addr3)
            val1 = mem[addr1] if (safe_list_get(modes,0,'0') == '0') else addr1
            val2 = mem[addr2] if (safe_list_get(modes,1,'0') == '0') else addr2
            x = val1 + val2
            print("     Sum",val1,val2,x,"Store in",addr3)
            mem[addr3] = x

        elif (instr == 2):     # Multiply operation
            opsize = 4
            addr1 = mem[ip+1]
            addr2 = mem[ip+2]
            addr3 = mem[ip+3]
            print("     ",addr1,addr2,addr3)
            val1 = mem[addr1] if (safe_list_get(modes,0,'0') == '0') else addr1
            val2 = mem[addr2] if (safe_list_get(modes,1,'0') == '0') else addr2
            x = val1 * val2
            print("     Prod",val1,val2,x,"Store in",addr3)
            mem[addr3] = x
        
        elif (instr == 3):      # input oper
            opsize = 2
            addr1 = mem[ip+1]
            print("     ", addr1)
            val1 = input("Program requesting input: ")
            mem[addr1] = int(val1)
            
        elif (instr == 4):      # save oper
            opsize = 2
            addr1 = mem[ip+1]
            print("     ", addr1)
            val1 = mem[addr1] if (safe_list_get(modes,0,'0') == '0') else addr1
            print("     Loaded",val1)
            outputs.append((val1,ip))            
        
        elif (instr == 99):    # Terminate
            print("Execution completed at", ip, "in", opCount, "instructions!")
            return mem
        else:
            print("Undefined command encountered at", ip, "Dumping memory.")
            print(mem)
            return mem
        
        ip += opsize

print("+---------------------------------+")
print("|      INTCODE MACHINE v0.01      |")
print("+---------------------------------+")

prgmIn = input("Enter Intcode Program:\n")
#nounIn = input("Noun Required: ")
#verbIn = input("Verb Required: ")
original = [int(i) for i in prgmIn.split(",")]            
output = runProgram(prgmIn)

print(outputs)
#for i in range(len(original)):
    #print(i,original[i],output[i])
