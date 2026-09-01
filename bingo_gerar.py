
import random

# quantas por página
por_pessoa = 3 

# quantas, por página, já estarão completas
gratuitas = 1 

quantidade = 100 # páginas

# para todas as páginas (do gabarito e das cartelas) poderem ser impressas de 4 em 4 (sem deixar nada em branco)
quantidade += 24 - (quantidade % 24)
total = quantidade * por_pessoa # cartelas

# nomes dos arquivos \cartela
CARTELAS_TEX = 'normal.tex' 	# uma pronta e duas parcialmente completas por página
DESAFIOS_TEX = 'problema.tex' 	# exigem equações, extras para quem quer mais cartelas 
GABARITO_TEX = 'respostas.tex' 	# quadrados completos

from bingo_sortear import CARTELAS, MAIOR, MENOR 

def quadr_magi (a, b, c):
	return [
		[c - b,	c + (a + b),	c - a],
		[c - (a - b),	c,	c + (a - b)],
		[c + a,	c - (a + b),	c + b]
	]

def tudo (ini = MENOR, fim = MAIOR):
	''' Salvar todos os parâmetros válidos em um TSV
	param = open('parâmetros.tsv', 'w')
	print('a','b','c',sep='\t',file=param)
	f = [{}, {}, {}]
	# '''

	for a in range(1, MAIOR):
		for b in range(a + 1, MAIOR):
			if b == 2 * a:
				continue

			for c in range(a + b + 1, MAIOR):
				if a + b + c > MAIOR or c - a - b < MENOR or b >= c - a:
					continue			

				''' # registrando os dados no TSV 			
				print(a,b,c,sep='\t', file=param)
				v = a,b,c # e contando para o CSV dos gráficos
				for k in range(len(v)):
					x = v[k]
					if x in f[k]:
						f[k][x] += 1
					else:	
						f[k][x] = 1
				#'''		

				yield (a, b, c)

	''' 
	param = open('parâmetros.csv', 'w')
	fk = [list(freq) for freq in f]
	while sum(len(freq) for freq in fk):
		ln = []
		k = 0

		for freq in fk:
			if len(freq):
				freq = freq.pop()
				ln.extend([freq, f[k][freq], ''])
			else:
				ln.extend([''] * 3)	

			k += 1	

		print(*ln, file=param, sep=',')	
	#	'''

def fileiras (n):

	dia = []
	sec = []
	for i in range(n):
		dia.append((i,i))
		sec.append((i,n-1-i))

		ln = []
		col = []
		for j in range(n):
			ln.append((i,j))
			col.append((j,i))
		yield ln
		yield col
	yield dia	
	yield sec
	
	yield dia	
	yield sec

			
cartelas = []
usadas = {}


if __name__ == '__main__':
	cartelas_txt = open(CARTELAS, 'w')
	cartelas_tex = open(CARTELAS_TEX, 'w')
	gabarito_tex = open(GABARITO_TEX, 'w')
	print('Calculando....')

	todas = list(tudo())
	print(len(todas), 'cartelas')

	while len(cartelas) < total and len(todas) > 0:
		
		r = random.randint(0, len(todas) - 1)
		v = list(todas.pop(r))
		v.sort()
		print(v, r)

		k = tuple(v) # a b c positivos e ordenados

		if k in usadas:
			print('Parâmetros já utilizados antes')
			continue 

		c = v.pop(-1) # constante central	

		if random.random() > 0.5: # reflexão horizontal
			v = v[::-1] # troca a e b de lugar

		v = [d if random.random() > 0.5 else -d for d in v]	+ [c]	 	
		print(v)

		c = quadr_magi(*v)	
		print(c)
		
		x = {col for ln in c for col in ln}
		if len(x) < len(c) ** 2:
			print('Há números repetidos')
			continue
		x = list(x)
		x.sort()
		x = tuple(x)
		print(x)

		if x in usadas:
			print('Conjunto já foi utilizado')
			continue
		if x[0] < MENOR or x[-1] > MAIOR:
			print('Cartela fora do intervalo')
			continue

		usadas[x] = k
		usadas[k] = x
		cartelas.append(c) 
		print(len(cartelas), '\n')	

		
		
		print(*k, ':\t', ';\t'.join(', '.join(f'{col:2}' for col in ln) for ln in c), file=cartelas_txt)

		mantido = {(i,j) for i in range(len(c)) for j in range(len(c[i]))}
		
		if len(cartelas) % por_pessoa == 1:
			trios = list(fileiras(len(c))) 
			print('\n\\newpage\t', len(cartelas), file=cartelas_tex)
			print('\n\\vfill\t\\subsubsection*{', len(cartelas), '}', file=gabarito_tex)
		else:	
			mantido = set(trios.pop(random.randint(0, len(trios) - 1)))
			
			while len(mantido) == len(c):
				mantido.add(tuple(random.randint(0, len(c) - 1) for k in range(2)))
			
			print('Manter:', mantido)	
		
		
		print('\\cartela{' + (
				'}{'.join(
					f'{c[i][j]:2}' 
					if (i,j) in mantido
					else '{\\color{white}XX}'
					for i in range(len(c)) 
					for j in range(len(c[i]))
				)
			) + '}', file=cartelas_tex)
		
		print('\\cartela{' + (
				'}{'.join(
					f'{col:2}' 
					for ln in c 
					for col in ln
				)
			) + '}', file=gabarito_tex)

	print('Sobrou', len(todas))
print(list(fileiras(3)))	