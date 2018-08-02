# coding=utf8

a = True
while a:
    number = input('请输入行数：')
    result = [[1], [1, 1]]
    for i in range(0, number-2):
        lst_pre = result[-1]
        lst = [1]
        for j in range(len(lst_pre)-1):
            lst.append(lst_pre[j]+lst_pre[j+1])
        lst.append(1)
        result.append(lst)

    length = number-1
    for i in result[-1]:
        length += len(str(i))

    for i in result:
        length_this = result.index(i)
        for j in i:
            length_this += len(str(j))
        print ' '*((length-length_this)/2),
        for k in i:
            print k,
        print
    b = raw_input("继续请输入Y")
    if b != 'Y':
        a = False
