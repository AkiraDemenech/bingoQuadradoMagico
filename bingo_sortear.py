
import random 

# mínimo e máximo para sorteio
MENOR = 1 
MAIOR = 60

CARTELAS = 'bingo.txt' # arquivo com todas as cartelas
SORTEIO = 'bingo.log' # números sorteados

sorteados = []
esperando = []
info = {
	n: []
	for n in range(MENOR, MAIOR + 1)
}

dividido = 1
for n in info:
	k = n
	d = 2
	fatores = []
	while k >= d: # fatores
		while k % d == 0:
			k //= d
			fatores.append(d)
		d += 1		
	
	k = n		
	d = 1
	divisores = set()
	while k >= d: # divisores
		k = n
		if n % d == 0:
			k //= d
			divisores.add(d)
			divisores.add(k)
		d += 1	
	divisores = list(divisores)
	divisores.sort()	

	# primeiro os fatores primos e os divisores
	info[n].append(fatores)
	info[n].append(divisores)

	info[n].append(bin(n))
	info[n].append(oct(n))
	info[n].append(hex(n))

	if len(divisores) > dividido:
		dividido = len(divisores)
		info[n].append(f'Altamente composto {len(divisores)}')	

	if sum(divisores) == 2 * n: # perfeito
		info[n].append('Perfeito')

#	elif len(fatores) == 1:
	elif len(divisores) == 2:
		info[n].append('Primo')	

		if (n - 2) in info and len(info[n-2][1]) == 2:
			info[n].append(f'Gêmeo {n-2}')
			info[n-2].append(f'Gêmeo {n}')

			info[n-1].append(f'Entre gêmeos {n-2} {n}')
	
	

# Triangulares 	
t = a = 0
while t < MAIOR:
	if t in info:
		info[t].append(f'Triangular {a}')
	a += 1
	t += a

# Fibonacci
a = c = 0
b = 1
while a < MAIOR:
	if a in info:
		info[a].append(f'Fibonacci {c}')
	a, b = b, a + b
	c += 1	

if __name__ == '__main__':
	print('Sortear bingo!')

	for n in info:
		print(n, *info[n], sep='\t')

	for ln in open(SORTEIO, 'r'):
		for col in ln.split():
			if col.isdigit:
				sorteados.append(int(col))
			else:	
				print(col)

	esperando.extend(n for n in range(MENOR, MAIOR + 1) if n not in sorteados)		
	print(esperando)

	rep = True
	while len(esperando) > 0 and rep:
		print(*sorteados)
		s = list(sorteados)
		s.sort()
		print('\n\t',*s)
		n = esperando.pop(random.randint(0, len(esperando) - 1))
		sorteados.append(n)
		print('\n', n, *info[n], sep='\n')

		
		e = input().strip().upper()
		rep = (e != 'SAIR')
		if e == 'ENCERRAR':
			break
		if e == 'LIMPAR':
			sorteados.clear()
			rep = False


		print(*sorteados[::-1], sep='\n', file=open(SORTEIO, 'w'))
	else:
		print('Fim dos números')