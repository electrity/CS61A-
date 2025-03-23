def casecode(n):
    if n < 10:
        print(n)
    else:
        print(n)
        casecode(n // 10)
        print(n)
    return 'here is the end'

print('\n',casecode(1232422),sep='',end='')