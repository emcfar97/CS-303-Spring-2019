import sympy

def addition(start, end, num):

    global matrix

    print(f'\nR{sub[end]}{num:+}R{sub[start]}')

    matrix = matrix.elementary_row_op(
        'n->n+km', row1=start-1, row=end-1, k=num
        )
    sympy.pprint(matrix)

def multiply(start, num):

    global matrix

    print(f'\n{num}R{sub[start]}')
    
    matrix = matrix.elementary_row_op(
        'n->kn', row=start-1, k=num
        )
    sympy.pprint(matrix)

def exchange(start, end):

    global matrix

    print(f'\nR{sub[start]} <-> R{sub[end]}')
    
    matrix = matrix.elementary_row_op(
        'n<->m', row1=start-1, row2=end-1
        )
    sympy.pprint(matrix)

def transpose():

    global matrix

    print('\nTranspose matrix')

    matrix = matrix.transpose()
    sympy.pprint(matrix)

sub = [chr(i) for i in range(8320, 8330)]

matrix = sympy.Matrix([
    [],
    ])

sympy.pprint(matrix)
print('\n', matrix.rref())
