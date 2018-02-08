.text

.globl _start

_start:
    movq $60, %rax
    movq $0, %rdi
    syscall
