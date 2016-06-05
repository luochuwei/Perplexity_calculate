#-*- coding:utf-8 -*-

import cPickle

ok_list = cPickle.load(open(r'ok-list.pkl', 'rb'))

f = open(r'test_nba2-500.txt')

fw = open(r'testfile.txt', 'w')

for num, line in enumerate(f):
    if num in ok_list:
        fw.write(line)


fw.close()
f.close()