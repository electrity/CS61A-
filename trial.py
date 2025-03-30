# 定义一个函数，用于判断一个数是否为偶数
def is_even(x):
    return x % 2 == 0

numbers = [1, 2, 3, 4, 5, 6]
# 使用 filter 函数过滤出偶数
result = filter(is_even, numbers)
# 将迭代器转换为列表
print(next(result))
even_numbers = list(result)
print(even_numbers)

class MyClass:
    class_attribute = 10

    def __init__(self,name):
        self.instance_attribute = 20

a = MyClass('jack')
b = MyClass('tom')
print(MyClass.class_attribute)
a.class_attribute = 20
print(MyClass.class_attribute)
print(b.class_attribute)
print(a.class_attribute)