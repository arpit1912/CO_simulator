.data
.word 7, 120, 8, 5, 2
.globl main

lw $a1, 0($a0)
lw $a3, 4($a0)
add $a3,$a1,$a2
add $a2,$a4,$a1
