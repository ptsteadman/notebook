# Hewwo World

.data

msgString:
    .ascii "Hewwo World :3\n"

.text

.globl _start

_start:
    movq $1, %rax
    movq $1, %rdi
    movq $msgString, %rsi
    movq $15, %rdx
    syscall
    movq $60, %rax
    movq $0, %rdi
    syscall
