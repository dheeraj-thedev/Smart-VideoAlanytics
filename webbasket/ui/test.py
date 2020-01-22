from functools import reduce

def Mul(a,b):
    return a*b

l = [1,2,3,4]
product = reduce(Mul, l)
print(product)
#product = list( map(Mul, l))
#print(product)

#
# l = [1,2,3,4]
#
#total = reduce(lambda x, y: x + y, l, 10)