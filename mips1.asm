.data 


vetor: .word 0:120

.text

	li $t0, 1 # cria no registrador v1 o valor 0, que será a variável de controle
	la $t3, vetor

inicio:	
		
	
	
	mul $t2, $t0, $t0 # Multipica e guarda em $t2
	
	li $v0,1 # O 1 tem a função de dar print
	move $a0, $t2 # Move $t2 para $a0
	syscall
	
			
	add $t0, $t0, 1 #p = p + 1
	sw $t2, ($t3)
	
	add $t3, $t3, 4

	ble $t0, 10, inicio # se for >= 10 vai para a fim, pois quero que vá até 10 ao quadrado
		
fim:

	
