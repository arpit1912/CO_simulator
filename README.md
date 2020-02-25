# CO_simulator

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
