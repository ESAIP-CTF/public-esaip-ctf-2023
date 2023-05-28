BITS 64

section .text
global _start

correct db "correct", 0xa, 0x0
correct_len equ $-correct
incorrect db "incorrect", 0xa, 0x0
incorrect_len equ $-incorrect

_start:
sub rsp, 40
mov rax, 0
mov rdi, 0
push rsp
pop rsi
mov rdx, 4
syscall

mov r8, 0
mov r9b, 0x4c

; check input
mov byte dl, [rsp + r8]
xor dl, r9b
cmp dl, 0x7d
jne print_incorrect

add r8, 1
mov byte dl, [rsp + r8]
xor dl, r9b
cmp dl, 0x75
jne print_incorrect

add r8, 1
mov byte dl, [rsp + r8]
xor dl, r9b
cmp dl, 0x74
jne print_incorrect

add r8, 1
mov byte dl, [rsp + r8]
xor dl, r9b
cmp dl, 0x7f
jne print_incorrect

; print input
;mov byte [rsp + 4], 0xa
;mov rax, 1
;mov rdi, 1
;mov rdx, 5
;syscall

print_correct:
; print correct
mov rax, 1
mov rsi, correct
mov rdi, 1
mov rdx, correct_len
syscall
jmp exit

print_incorrect:
; print incorrect
mov rax, 1
mov rsi, incorrect
mov rdi, 1
mov rdx, incorrect_len
syscall
jmp exit

exit:
; exit
add rsp, 64
mov rax, 60
mov rdi, 0
syscall
