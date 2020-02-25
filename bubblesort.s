.data

array: .word 7, 120, 8, 5, 2, 3, 9, 10, 55, 1, 4

.text

.globl main

main:

add $a2,$d1,$d1
add $a8,$d1,$d1
addi $a8,$a8,1

addi $a2,$a2,10

loop1:
beq $a2,$d1,end


	add $a5,$d1,$d1

	la $a0, 0x10000000
	addi $a1,$a0,4
loop2:	
	beq $a2,$a5,loop3
		lw $a3, 0($a0)
		lw $a4, 0($a1)
		slt $a6,$a3,$a4
		bne $a6,$d1,jmp
		sw $a3, 0($a1)
		sw $a4, 0($a0)
		j jmp2
	jmp:	
		sw $a3, 0($a0)
		sw $a4, 0($a1)

	jmp2:
		addi $a5,$a5,1	
		addi $a0,$a0,4
		addi $a1,$a1,4
	j loop2
loop3:
	sub $a2,$a2,$a8
	j loop1
end:


jr $ra


