# Demo of various data types

.data
    HelloWorld:
        .ascii "Hello world!"
    ByteLocation:
        .byte 10
    Int:
        .int 2
    Float:
        .float 42.42
    IntegerArray
        .int 10,50,100

.bss
    .comm LargeBuffer, 10000

.text

    .globl _start
