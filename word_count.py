# coding:utf8

import re

def pick_up_file(filename):
    with open(filename) as f:
        content = f.readlines()
    count = 0
    for i in content:
        result = re.findall(r"\b[A-z]+\b",i)
        count += len(result)
    return count

if __name__ == '__main__':
    print '共计单词数：%s' %pick_up_file('file.txt')
