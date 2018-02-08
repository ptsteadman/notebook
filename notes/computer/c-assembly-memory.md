# Assembly / Reversing 

### General Purpose CPU Registers: 

EAX: Accumulator Register - used for storing operands and result data
EBX: Base Register - pointer to data
ECX: Counter Register - loop operations
EDX: Data Register

AX: 0 - 15 bits of EAX
AL: 0 - 7 bits of EAX
AH: 8 - 15 bits of EAX

ESI EDI: Data Pointer Registers
ESP: points to top of the stack
EBP: stack data pointer register


### Segment Registers:

CS: Code Segment
DS: Data Segment
SS: Stack Segment
ES FS GS

### Instruction Pointer Register:

EIP -> points to instruction CPU is currently executing

### Control Registers:

CR0 CR1 CR2 CR3


### Program Memory

0xBFF

Stack: grows down, LIFO
Unused Memory
Heap
.bss
.data
.text

0x000

To view current memory layout map:

- Find pid using ps -aux | grep 
- cat /proc/${pid}/maps

To turn off ASLR:

sudo su
echo 0 > /prod/sys/kernel/randomize_va_space

### Linux System Calls

full list at /usr/include/asm/unistd.h

i386
How to pass args to syscall: EAX is syscall number, EBX 1st arg, ECX 2nd arg
system calls are invoked by processes using a software interrupt: INT 0x80

x86_64
rax(rdi, rsi, rdx, r10, r8)
syscall op

