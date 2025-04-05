"""# 定义一个函数，用于判断一个数是否为偶数
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

def search(query, ranking=lambda r: -r.stars):
    results = [r for r in Restaurant.all if query in r.name]
    return sorted(results, key=ranking)

class Restaurant:
    all = []
    def __init__(self, name, stars):
        self.name, self.stars = name, stars
        Restaurant.all.append(self)

    def similar(self, k, similarity):
        "Return the K most similar restaurants to SELF, using SIMILARITY for comparison."
        others = list(Restaurant.all)
        others.remove(self)
        return sorted(others, key= lambda r: -similarity(self,r))[:k]

    def __repr__(self):
        return '<' + self.name + '>'

import json

reviewers_for_restaurant = {}
for line in open('reviews.json'):
    r = json.loads(line)
    biz = r['business_id']
    if biz not in reviewers_for_restaurant:
        reviewers_for_restaurant[biz] = [r['user_id']]
    else:
        reviewers_for_restaurant[biz].append(r['user_id'])

for line in open('restaurants.json'):
    r = json.loads(line)
    reviewers = reviewers_for_restaurant[r['business_id']]
    Restaurant(r['name'], r['stars'], reviewers)

Restaurant('Thai Delight', 2)
Restaurant('Thai Basil', 3)
Restaurant('Top Dog', 5)

results = search('Thai')
for r in results:
    print(r, 'is similar to', r.similar(3))"""

"""class Worker:
    greeting = 'Sir'
    def __init__(self):
        self.elf = Worker
    def work(self):
        return self.greeting + ', I work'
    def __repr__(self):
        return Bourgeoisie.greeting

class Bourgeoisie(Worker):
    greeting = 'Peon'
    def work(self):
        print(Worker.work(self))
        return 'I gather wealth'

jack = Worker()
john = Bourgeoisie()
a = jack.work()
b = john.work()
#print(jack.work())
#print(john.work())
#print(jack)
#print(john)
print(repr(john.elf.work(john)))"""

"""s = [1, 2, 3, 4, 5, 6, 3]
def cheak(list):
    return all(list[i] in list[:i] + list[i + 1:] for i in range(len(list)))

print(cheak(s))"""

"""class Link:"""

from math import pow

def reduce(f,s,x):
    result = x
    if s:
        return reduce(f,s[1:],f(result,s[0]))
    else:
        return x


print(reduce(pow,[1,2,3],204))

