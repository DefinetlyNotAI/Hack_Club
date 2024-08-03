; calc_2.asm
[bits 32]

section .data
    prompt db 'Enter first number: ', 0
    prompt2 db 'Enter second number: ', 0
    promptOp db 'Enter operation (+/-/*/): ', 0
    resultMsg db 'Result: ', 0
    newline db 10, 0 ; Newline character

section .bss
    num1 resq 1
    num2 resq 1
    op resb 1
    result resq 1

section .text
    extern printf
    extern scanf

    global main
    global _start

_start:
    ; Call main function
    jmp main

main:
    ; Prepare strings for printing
    ; For printf, the format string is passed in EAX, but since we're using string literals,
    ; we don't need to manually move anything into EAX. The call to printf will automatically
    ; use the string literal as the format string.
    mov edi, prompt
    call printf

    ; Read first number
    ; For scanf, the address of the variable is passed in ECX, and the variable itself in EDX.
    mov ecx, num1
    mov edx, num1
    call scanf

    ; Prepare strings for printing
    mov edi, prompt2
    call printf

    ; Read second number
    mov ecx, num2
    mov edx, num2
    call scanf

    ; Prepare strings for printing
    mov edi, promptOp
    call printf

    ; Read operation
    mov edi, op
    call scanf

    ; Placeholder for operation logic
    ; You need to implement the logic to perform the operation based on the value in 'op'
    ; For example, if op is '+', add num1 and num2, store the result in 'result', and convert it to a string

    ; Display result
    ; Assuming 'result' contains the result of the operation as a string
    mov edi, resultMsg
    call printf

    ; Exit program
    ; Correct system call for exiting the program
    mov eax, 1 ; System call number for exit
    xor ebx, ebx ; Status 0
    int 0x80 ; Trigger interrupt
