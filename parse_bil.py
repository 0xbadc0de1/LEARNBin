import binascii

def is_x64reg(x):
    y = x.strip()
    return y in ["RAX", "RBX", "RCX", "RDX", "RDI", "RSI",
            "R8", "R9", "R10", "R11", "R12", "R13", "R14", "R15", "RSP", "RIP", "RBP"]

def is_bitflag(x):
    
    y = x.strip()
    return y in ["ZF", "OF", "SF", "PF", "AF", "TF", "IF", "DF", "IOPL", "NT", 
            "RF", "VM", "AC", "VIF", "VIP", "ID"]

class operator:
    
    def __init__(self, bit_sz):
        self.bit_sz = bit_sz
        return
    def __str__(self):
        raise Exception("operator string cast not implemented.")


class mon_op(operator):

    def __init__(self, operand1, bit_sz):
        operator.__init__(self, bit_sz)
        self.op1 = operand1
        return

    def __str__(self):
        raise Exception("mon_op string cast not implemented!")

class bin_op(operator):

    def __init__(self, op1, op2, bit_sz):
        operator.__init__(self, bit_sz)
        self.op1=op1
        self.op2=op2
        return

    def __str__(self):
        raise Exception("bin_op string cast not implemented.")

class tern_op(operator):

    def __init__(self, op1, op2, op3, bit_sz):
        operator.__init__(self, bit_sz)
        self.op1=op1
        self.op2=op2
        self.op3=op3
        return

    def __str__(self):
        raise Exception("bin_op string cast not implemented.")


#Always loads unsigned.
class memref(mon_op):

    def __init__(self, address, bit_sz)
        mon_op.__init__(self, address, bit_sz)
        return

    def __str__(self):
        return "mem[ " + str(self.op1) + ", el ]" + ":[00:"+str(self.bit_sz) + "]"

class arg_in(operand)
    
    def __init__(self, arg_name, bit_sz):
        operand.__init__(self, bit_sz)
        self.arg_name = arg_name
        return

    def __str__(self):
        return "arg (in) " + self.arg_name + ":[00:"+str(self.bit_sz) + "]"

class arg_out(operand):

    def __init__(self, arg_name, bit_sz):
        operand.__init__(self, bit_sz)
        self.arg_name = arg_name
        return

    def __str__(self):
        return "arg (out) " + self.arg_name + ":[00:"+str(self.bit_sz) + "]"

class operand:

    def __init__(self, bit_sz):
        self.bit_sz = bit_sz
        return
    
    def __str__(self):
        return "[00:" + str(self.bit_sz) + "]"

class x64_reg (operand):

    def __init__(self, reg_name, ssa_index):
        operand.__init__(self, 64)
        self.reg_name = reg_name
        self.ssa_index = ssa_index
        return

    def __str__(self):
        return self.reg_name + "." + str(self.ssa_index) + operand.__str__(self)


class tmp_var(operand):

    def __init__(self, var_index, ssa_index, bitsz):
        operand.__init__(self, bitsz)
        self.var_index = var_index
        self.ssa_index = ssa_index
        return

    def __str__(self):
        return "v"+str(self.var_index)+"."+str(self.ssa_index) + operand.__str__(self)


class bitvect(operand):

    def __init__(self, bitsz, value):
        operand.__init__(self, bitsz)
        self.value = value % (1<<bitsz)
        return

    def __str__(self):
        return hex(self.value) + operand.__str__(self)


class flag_bit(operand):

    def __init__(self, flag_bit):
        operand.__init__(self, 1)
        self.flag_bit = flag_bit
        return

    def __str__(self):
        return self.flag_bit + operand.__str__(self)

class memory_space(operand):

    def __init__(self, ssa_index):
        operand.__init__(self, None)
        self.ssa_index = ssa_index
        return

    def __str__(self):
        return "mem" + "." + str(self.ssa_index)

#Virtual address (the abstracted address)
class vaddr(operand):

    def __init__(self, address):
        operand.__init__(self, 64)
        self.address = address
        return

    def __str__(self):
        return "VADDR: [ " + hex(self.address).strip("L") + " ]"

class func_ref(operand):

    def __init__(self, fname):
        operand.__init__(self, None)
        self.fname = fname
        return

    def __str__(self):
        return "@" + self.fname

class function:

    def __init__(self, arg_list, fname):
        self.arg_list = arg_list
        self.fname = fname
        self.instrs = []
        return

    def add_instruction(self, instr):
        self.instrs.append(instr)
        return

    def __str__(self):
        data = ""
        data += self.fname + "( "
        for arg in self.arg_list:
            data += str(arg) + ", "

        data += " ):"
        for instr in self.instrs:
            data += instr + "\n"
        return data



###################################################
#                                                 #
#                Unary  Operators                 #
#                                                 #
###################################################


class high_bit(mon_op):

    def __init__(self, bits, operand):
        mon_op.__init__(self, operand, bits)
        assert(bits <= operand.bit_sz)
        return

    def __str__(self):
        return "high:"+str(self.bits) + str(self.operand)

class low_bit(mon_op):

    def __init__(self, bits, operand): 
        mon_op.__init__(self, operand, bits)
        assert(bits <= operand.bit_sz)
        return

    def __str__(self):
        return "low:"+str(self.bit_sz) + str(self.operand)

class pad(mon_op):

    def __init__(self, bits, operand):
        mon_op.__init__(self, operand, bits)
        assert(bits >= operand.bit_sz)
        return

    def __str__(self):
        return "pad:"+str(self.bit_sz) + str(self.operand)

class retn(mon_op):

    def __init__(self, op1):
        return

    def __str__(self):
        return "return " + str(self.op1)

###################################################
#                                                 #
#                Binary Operators                 #
#                                                 #
###################################################

class add(bin_op):

    def __init__(self, op1, op2):
        assert(op1.bit_sz == op2.bit_sz)
        bin_op.__init__(self, op1, op2, op1.bit_sz)
        return

    def __str__(self):
        return str(self.op1) + " + " + str(self.op2)

class sub(bin_op):

    def __init__(self, op1, op2):
        assert(op1.bit_sz == op2.bit_sz)
        bin_op.__init__(self, op1, op2, op1.bit_sz)
        return

    def __str__(self):
        return str(self.op1) + " - " + str(self.op2)

class call_op(bin_op):

    def __init__(self, op1, op2):
        assert(isinstance(op1, func_ref))
        assert(isinstance(op2, vaddr))
        bin_op.__init__(self, op1, op2, None)
        return

    def __str__(self):
        return "call " + str(self.op1) + ", and return: " + str(self.op2)

class assign(bin_op):

    def __init__(self, op1, op2):
        bin_op.__init__(self, op1, op2, None)
        return


    def __str__(self):
        return str(self.op1) + " := " + str(self.op2)


class test(bin_op):

    def __init__(self, op1, op2):
        assert(op1.bit_sz == op2.bit_sz)
        bin_op.__init__(self, op1, op2, 1) # testing is usually 1 bit
        return



###################################################
#                                                 #
#               Ternary Operators                 #
#                                                 #
###################################################


class mem_store(tern_op):

    def __init__(self, old_mem, mem_ref, value):
        assert(isinstance(mem_ref, memref))
        assert(mem_ref.bit_sz == value.bit_sz)
        assert(isinstance(old_mem, memory_space))
        tern_op.__init__(self, old_mem, mem_ref, value, None)
        return

    def __str__(self):
        return str(self.op1) + " with " + str(self.op2) + " <- " + str(self.op3)



if __name__ == "__main__":
    
    print "work-in-progress parser for BAP-IL."
