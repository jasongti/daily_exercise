# coding:utf8

N = []
for i in range(1,2021):
    if 2020%i == 0:
        N.append(i)
N = N[1:-1]

resultA = {}
for j in N:
    for a in range(1,2001):
        for b in range(1,2001):
            if (j - a * a) % b == 0:
                z = (j - a * a) / b
            if z == b and j not in resultA:
                resultA[j] = [a,b]
print resultA


