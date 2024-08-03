section .data
    prompt db 'Enter first number: ', 0
    prompt2 db 'Enter second number: ', 0
    promptOp db 'Enter operation (+/-/*/): ', 0
    resultMsg db 'Result: ', 0

section .bss
    num1 resd 1
    num2 resd 1
    op resb 1
    result resd 1

section .text
    global _start

_start:
    ; Prompt for first number
    mov eax, 4
    mov ebx, 1
    mov ecx, prompt
    mov edx, 21
    int 0x80

    ; Read first number
    mov eax, 3
    mov ebx, 0
    mov ecx, num1
    mov edx, 4
    int 0x80

    ; Convert ASCII to integer
    sub byte [num1], '0'

    ; Prompt for second number
    mov eax, 4
    mov ebx, 1
    mov ecx, prompt2
    mov edx, 24
    int 0x80

    ; Read second number
    mov eax, 3
    mov ebx, 0
    mov ecx, num2
    mov edx, 4
    int 0x80

    ; Convert ASCII to integer
    sub byte [num2], '0'

    ; Prompt for operation
    mov eax, 4
    mov ebx, 1
    mov ecx, promptOp
    mov edx, 26
    int 0x80

    ; Read operation
    mov eax, 3
    mov ebx, 0
    mov ecx, op
    mov edx, 2
    int 0x80

    ; Perform operation
    cmp byte [op], '+'
    je add
    cmp byte [op], '-'
    je subtract
    cmp byte [op], '*'
    je multiply
    cmp byte [op], '/'
    je divide
    jmp exit

add:
    mov eax, [num1]
    add eax, [num2]
    jmp displayResult

subtract:
    mov eax, [num1]
    sub eax, [num2]
    jmp displayResult

multiply:
    mov eax, [num1]
    imul eax, [num2]
    jmp displayResult

divide:
    mov eax, [num1]
    idiv dword [num2]
    jmp displayResult

displayResult:
    ; Display result message
    mov eax, 4
    mov ebx, 1
    mov ecx, resultMsg
    mov edx, 9
    int 0x80

    ; Exit
exit:
    mov eax, 1
    xor ebx, ebx
    int 0x80
