.data
.text
check .word 23, 12,123
.globl main

beq $a1,$a2,label2
sub $a3,$a1,$a2
label2:
add $a3,$a1,$a2
