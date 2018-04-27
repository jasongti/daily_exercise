# coding:utf-8

import re

def pickup(filename):
    with open(filename,'r') as f:
        a = f.read()
        lst = re.findall(r"\b[a-zA-Z]+\b", a)
        lst.sort()
    return lst
def write_the_result(lst):
    with open('to.txt','w') as f:
        f.write('\n'.join(str(i) for i in lst))

if __name__ == "__main__":
    write_the_result(pickup("from.txt"))