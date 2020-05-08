# CO_simulator Phase 1

MIPS simulator (phase 1)

Programming language used: Python

Memory supported: 4KB
	Address from 0x10000000-0x10000fff

32 registers:   $a0-$a9, $b0-$b9, $c0-$c9, $d0, $d1
		$d1 is synonomous with $zero
		other registers can be given specific functionality later on as required

instructions supported: lw,la,sw,add,sub,bne,beq,j,slt

data type supported: word

Additional features: basic GUI to show registers and memory states, buttons for single and multi step execution

#CO_simulator Phase 2

Now the basic stalls are calculated by our simulator

We are displaying the output using the console.
The file for the code is simulator_with_cycle_calculation.py which uses bubblesort.s as an input of MIPS instruction

# now the simulator with latency will help in calculating the latency due to the memory access, there is a two level cache that is present in the simulator with LRU policy for the inputs we uses input.txt as a input file
