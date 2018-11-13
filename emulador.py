
memory = [ ]
memory_size = 64
regs = [0, 0, 0, 0, 0, 0, 0, 0]
cpu_alive = True
cycle = 0

reg_pc = 0
reg_inst = 0

decoded_inst = {
	'type'        : 0,
	'opcode'      : 0,

	'r_dest'      : 0,
	'r_op1'       : 0,
	'r_op2'       : 0,

	'i_reg'       : 0,
	'i_imed'      : 0,
	}

def extract_bits (num, bit_init, bit_len):
	num = num >> bit_init
	mask = (1 << bit_len) - 1
	return num & mask

def fetch () :
	global reg_pc, reg_inst
	print("Fetch addr " + str(reg_pc))
	reg_inst = memory[reg_pc]
	reg_pc = reg_pc + 1

def decode () :
	global reg_inst, decoded_inst

	print("Decode inst " + str(reg_inst))

	decoded_inst['type'] = extract_bits(reg_inst, 15, 1)

	if decoded_inst['type'] == 0:
		decoded_inst['opcode'] = extract_bits(reg_inst, 9, 6)
		decoded_inst['r_dest'] = extract_bits(reg_inst, 6, 3)
		decoded_inst['r_op1'] = extract_bits(reg_inst, 3, 3)
		decoded_inst['r_op2'] = extract_bits(reg_inst, 0, 3)
	else:
		decoded_inst['opcode'] = extract_bits(reg_inst, 13, 2)
		decoded_inst['i_reg'] = extract_bits(reg_inst, 10, 3)
		decoded_inst['i_imed'] = extract_bits(reg_inst, 0, 9)

def execute () :
	global decoded_inst, reg_pc, cpu_alive, regs, memory, memory_size

	print("Execute inst")
	print(decoded_inst)

	if decoded_inst['type'] == 0:
		# add
		if decoded_inst['opcode'] == 0:
			print("add r"+str(decoded_inst['r_dest'])+", r"+str(decoded_inst['r_op1'])+", r"+str(decoded_inst['r_op2']))
			regs[ decoded_inst['r_dest'] ] = regs[ decoded_inst['r_op1'] ] + regs[ decoded_inst['r_op2'] ]

		# sub
		elif decoded_inst['opcode'] == 1:
			print("add r"+str(decoded_inst['r_dest'])+", r"+str(decoded_inst['r_op1'])+", r"+str(decoded_inst['r_op2']))
			regs[ decoded_inst['r_dest'] ] = regs[ decoded_inst['r_op1'] ] - regs[ decoded_inst['r_op2'] ]

		#mul
		elif decoded_inst['opcode'] == 2:
			print("mul r"+str(decoded_inst['r_dest'])+", r"+str(decoded_inst['r_op1'])+", r"+str(decoded_inst['r_op2']))
			regs[ decoded_inst['r_dest'] ] = regs[ decoded_inst['r_op1'] ] * regs[ decoded_inst['r_op2'] ]

        # div
		elif decoded_inst['opcode'] == 3:
			print("mul r"+str(decoded_inst['r_dest'])+", r"+str(decoded_inst['r_op1'])+", r"+str(decoded_inst['r_op2']))
			regs[ decoded_inst['r_dest'] ] = regs[ decoded_inst['r_op1'] ] / regs[ decoded_inst['r_op2'] ]

		#cmp_eq
		elif decoded_inst['opcode'] == 4:
			print("cmp_neq r"+str(decoded_inst['r_dest'])+", r"+str(decoded_inst['r_op1'])+", r"+str(decoded_inst['r_op2']))
			if regs[ decoded_inst['r_op1']] == regs[ decoded_inst['r_op2']]:
				regs[ decoded_inst['r_dest']] = 1
			else:
				regs[ decoded_inst['r_dest'] ]= 0

		#cmp_neq
		elif decoded_inst['opcode'] == 5:
			print("cmp_neq r"+str(decoded_inst['r_dest'])+", r"+str(decoded_inst['r_op1'])+", r"+str(decoded_inst['r_op2']))
			if regs[ decoded_inst['r_op1']] != regs[ decoded_inst['r_op2']]:
				regs[ decoded_inst['r_dest']] = 1
			else:
				regs[ decoded_inst['r_dest'] ]= 0

		#load
		elif decoded_inst['opcode'] == 15:
			print(regs[ decoded_inst['r_op1']])
			regs[ decoded_inst['r_dest'] ] = memory[regs[ decoded_inst['r_op1']]]

		# store
		elif decoded_inst['opcode'] == 16:
			print(regs[ decoded_inst['r_op1']])
			memory[regs[ decoded_inst['r_op1']]] = regs[ decoded_inst['r_op2']]

		# halt
		elif decoded_inst['opcode'] == 63:
			print("halt")
			cpu_alive = False

		else:
			print("opcode " + str(decoded_inst['opcode']) + " invalido tipo R")
			cpu_alive = False
	elif decoded_inst['type'] == 1:
		# jump
		if decoded_inst['opcode'] == 0:
			print("jump "+str(decoded_inst['i_imed']))
			reg_pc = decoded_inst['i_imed']
		#jump_cond
		elif decoded_inst['opcode'] == 1:
			print("jump_cond "+str(decoded_inst['i_imed']))
			if regs[decoded_inst['i_reg']] == 1:
				reg_pc = decoded_inst['i_imed']
		#mov
		elif decoded_inst['opcode'] == 3:
			print("mov "+str(decoded_inst['i_imed']))
			regs[decoded_inst['i_reg']] = decoded_inst['i_imed']


		else:
			print("opcode " + str(decoded_inst['opcode']) + " invalido tipo I")
			cpu_alive = False
	else:
		print("instr type " + str(decoded_inst['type']) + " invalido")
		cpu_alive = False

	print(regs)


def cpu_loop () :
	global cycle

	print("---------------------------------")
	print("Cycle " + str(cycle))

	fetch()
	decode()
	execute()

	cycle = cycle + 1

def main () :
	global memory, memory_size, cpu_alive, regs

	for i in range(0, memory_size):
		memory.append(0x0000)
	print("Memory size (words): " + str(len(memory)))

	z = 0
	memory[z] = 0b1110000000000001    # mov r0, 1
	z = z + 1
	memory[z] = 0b1110100000001000    # mov r2, 8
	z = z + 1
	memory[z] = 0b1110010000000001    # mov r1, 1
	z = z + 1
	memory[z] = 0b1111000000010100    # mov r4, 20
	z = z + 1
	memory[z] = 0b0000010101001001    # mul r5, r1, r1
	z = z + 1
	memory[z] = 0b0010000000100101    # store [r4], r5
	z = z + 1
	memory[z] = 0b0000000100100000    # add r4, r4, r0
	z = z + 1
	memory[z] = 0b0000000001001000    # add r1, r1, r0
	z = z + 1
	memory[z] = 0b0000101011001010    # cmp_neq r3, r1, r2
	z = z + 1
	memory[z] = 0b1010110000000100    # jump_cond r3, 4
	z = z + 1
	memory[z] = 0b0111111000000000    # halt inst
	z = z + 1

	while cpu_alive:
		cpu_loop()

	print(regs)
	print(memory)

	print("pysim halted")

main()
