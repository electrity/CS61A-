'''def k_in_num(k, num):
    # 确定 num 的最大位数
    max_digit_place = 0
    temp_num = num
    while temp_num > 0:
        max_digit_place += 1
        temp_num //= 10

    # 遍历每一位数字，从最高位到最低位
    for i in range(max_digit_place - 1, -1, -1):
        digit = (num // (10 ** i)) % 10
        if k == digit:
            print('True')
            return

    print('False')


k = int(input('type k: '))
num = int(input('type num: '))
k_in_num(k, num)

def tow_of_three(a,b,c):
    max_digit = max(a,b,c)
    tuple1 = (a,b,c)
    totol = 0
    for x in tuple1:
        if x != max_digit:
            totol += x
    print(totol)
    return

a = int(input('输入一个数:'))
b = int(input('输入一个数:'))
c = int(input('输入一个数:'))

tow_of_three(a,b,c)

def largest_factor(n):
    list1 = []
    for i in range(n-1,1,-1):
        if n % i == 0:
            list1.append(i)
    list1.reverse()
    print(f'factors are {", ".join(map(str, list1))}')

n = int(input('type a intaget；'))

largest_factor(n)
'''






