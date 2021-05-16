# ASSUMPTION: Input sequences are either all in lower case or upper case letters
# In traceback matrix, 1: up; 2: diagonal; 3: left

def globalAlignment(seq1, seq2):

	matrix = [[0 for i in range(cols)] for j in range(rows)]	#create matrix
	ctr = 0
	#setting first row and column with gap penalties
	for j in range(cols):	
		matrix[0][j] = ctr
		ctr+=gap

	ctr = 0
	for i in range(rows):
		matrix[i][0] = ctr
		ctr+=gap

	#computing dynamic programming matrix
	for i in range(rows):
		for j in range(cols):
			if i>0 and j>0:
				top = matrix[i-1][j] + gap    #gap in sequence 1
				left = matrix[i][j-1] + gap    #gap in sequence 2
				if seq1[j-1] == seq2[i-1]:	#match
					diag = matrix[i-1][j-1] + match
				else:	#mismatch
					diag = matrix[i-1][j-1] + mismatch

				#taking max of 3 possibilities
				matrix[i][j] = max(top, left, diag)
	
	for row in matrix:
		print(row)

	print('\nOptimal score: ')
	print(matrix[rows-1][cols-1])
	print('\nAligned sequences: ')
	#backtrack from last element in matrix to find aligned sequences
	reconstruct(matrix, rows-1, cols-1, '', '', '')

def localAlignment(seq1, seq2):

	matrix = [[0 for i in range(cols)] for j in range(rows)]	#create matrix
	maxrow = 0
	maxcol = 0
	#computing dynamic programming matrix
	for i in range(rows):
		for j in range(cols):
			if i>0 and j>0:
				top = matrix[i-1][j] + gap    #gap in sequence 1
				left = matrix[i][j-1] + gap    #gap in sequence 2
				if seq1[j-1] == seq2[i-1]:	#match
					diag = matrix[i-1][j-1] + match
				else:	#mismatch
					diag = matrix[i-1][j-1] + mismatch

				#taking max of 3 possibilities
				maxval = max(top, left, diag)	

				if maxval<0:	#handling negative values
					matrix[i][j] = 0
				else:
					matrix[i][j] = maxval

				#finding position in matrix with max value
				if matrix[i][j] >= matrix[maxrow][maxcol]:	
					maxrow = i
					maxcol = j
	
	for row in matrix:
		print(row)

	print('\nOptimal score: ')
	print(matrix[maxrow][maxcol])
	print('\nAligned sequences: ')

	#backtrack from max element to find aligned sequences
	for i in range(rows):
		for j in range(cols): 
			if matrix[i][j] == matrix[maxrow][maxcol]:
				reconstructLocal(matrix, i, j, '', '', '') 

def reconstruct(matrix, rowpos, colpos, a1, a2, a3):	#generates optimal aligments
	if rowpos==0 and colpos==0:	#base case
		print(a1)
		print(a2)
		print(a3)
		return 

	if rowpos==0 and colpos!=0:
		if matrix[rowpos][colpos-1] == matrix[rowpos][colpos] - gap:
			reconstruct(matrix, rowpos, colpos-1, seq1[colpos-1] + a1, ' ' + a2, '_' + a3)
			return

	if rowpos!=0 and colpos==0:
		if matrix[rowpos-1][colpos] == matrix[rowpos][colpos] - gap:
			reconstruct(matrix, rowpos-1, colpos, '_' + a1, ' ' + a2, seq2[rowpos-1] + a3)
			return 

	if seq1[colpos-1] == seq2[rowpos-1]:
		if matrix[rowpos-1][colpos-1] == matrix[rowpos][colpos] - match:
			reconstruct(matrix, rowpos-1, colpos-1, seq1[colpos-1] + a1, '|' + a2, seq2[rowpos-1] + a3)

	if seq1[colpos-1] != seq2[rowpos-1]:
		if matrix[rowpos-1][colpos-1] == matrix[rowpos][colpos] - mismatch:
			reconstruct(matrix, rowpos-1, colpos-1, seq1[colpos-1] + a1, ' ' + a2, seq2[rowpos-1] + a3)

	if matrix[rowpos-1][colpos] == matrix[rowpos][colpos] - gap:
		reconstruct(matrix, rowpos-1, colpos, '_' + a1, ' ' + a2, seq2[rowpos-1] + a3)

	if matrix[rowpos][colpos-1] == matrix[rowpos][colpos] - gap:
		reconstruct(matrix, rowpos, colpos-1, seq1[colpos-1] + a1, ' ' + a2, '_' + a3)


def reconstructLocal(matrix, rowpos, colpos, a1, a2, a3):	#generates optimal aligments
	if matrix[rowpos][colpos] == 0:	#base case
		
		print(a1)
		print(a2)
		print(a3)
		return 

	if seq1[colpos-1] == seq2[rowpos-1]:
		if matrix[rowpos-1][colpos-1] == matrix[rowpos][colpos] - match:
			reconstructLocal(matrix, rowpos-1, colpos-1, seq1[colpos-1] + a1, '|' + a2, seq2[rowpos-1] + a3)

	if seq1[colpos-1] != seq2[rowpos-1]:
		if matrix[rowpos-1][colpos-1] == matrix[rowpos][colpos] - mismatch:
			reconstructLocal(matrix, rowpos-1, colpos-1, seq1[colpos-1] + a1, ' ' + a2, seq2[rowpos-1] + a3)

	if matrix[rowpos-1][colpos] == matrix[rowpos][colpos] - gap:
		reconstructLocal(matrix, rowpos-1, colpos, '_' + a1, ' ' + a2, seq2[rowpos-1] + a3)

	if matrix[rowpos][colpos-1] == matrix[rowpos][colpos] - gap:
		reconstructLocal(matrix, rowpos, colpos-1, seq1[colpos-1] + a1, ' ' + a2, '_' + a3)


seq1 = list(input('Sequence 1: '))	#input sequence 1
seq2 = list(input('Sequence 2: '))	#input sequence 2
match = int(input('Enter scoring function.\nMatch: '))	#input scoring function
mismatch = int(input('Mismatch: '))
gap = int(input('Gap: '))
cols = len(seq1) + 1
rows = len(seq2) + 1 
print('\nGlobal Alignment:\n')
globalAlignment(seq1, seq2)	#compute global alignment using dynamic programming
print('\nLocal Alignment:\n')
localAlignment(seq1, seq2)	#compute local alignment using dynamic programming
