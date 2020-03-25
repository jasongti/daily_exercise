import re

lst = ['127893423423', '464545623789', '13789']
result_lst = []

for i in lst:
    result = re.findall(r'^12\d*', i)
    result_lst.extend(result)
for j in result_lst:
    print j
