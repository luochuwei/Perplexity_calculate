#-*- coding:utf-8 -*-

import re
import cPickle
import jieba
import time
import math

import collections, nltk

from nltk.util import ngrams

def ngram_return_model(model, tokens_for_ngram, n):
    for f in ngrams(tokens_for_ngram, n, pad_left=True, pad_right=True, left_pad_symbol='<s>', right_pad_symbol='</s>'):
        try:
            model[f] += 1
        except KeyError:
            model [f] = 1
            continue
    return model




def perplexity_score(testset, model, n):
    testset = testset.split()
    perplexity = 1
    N = 0
    for word in ngrams(testset, n, pad_left=True, pad_right=True, left_pad_symbol='<s>', right_pad_symbol='</s>'):
        N += 1
        perplexity = perplexity * (1/model[word])
    perplexity = pow(perplexity, 1/float(N))
    return perplexity




pid_p_r_seg = cPickle.load(open(r'pid_p_r_seg-0604.pkl', 'rb'))


# a = pid_p_r[0][0]

# b = find_all_url(a, replace_urls=1)

# c = ' '.join(jieba.cut(b))

# d = delete_mark(c)

ngram_num = 5
model = collections.defaultdict(lambda: 0.01)

print "training ",ngram_num," model..."
for pid in pid_p_r_seg:
    in_start = time.time()
    
    post_seg = pid_p_r_seg[pid][0]

    for f in ngrams(post_seg.split(), ngram_num, pad_left=True, pad_right=True, left_pad_symbol='<s>', right_pad_symbol='</s>'):
        model[f] += 1

    for r_seg in pid_p_r_seg[pid][1]:
        for ff in ngrams(post_seg.split(), ngram_num, pad_left=True, pad_right=True, left_pad_symbol='<s>', right_pad_symbol='</s>'):
            model[ff] += 1
        
    in_time = time.time() - in_start
    print "id : ", pid, "  Time : ", in_time


for word in model:
    model[word] = model[word]/float(len(model))


f = open(r'nba2-0.03.output')
fp = open(r'POS-nba2-0.122.output')

# f = open(r'nba2-500-0.107-out.txt')
# fp = open(r'POS-nba2-500-0.122-out.txt')

s2s_simple_p_list = []
s2s_pos_p_list = []

ok_list1 = []
ok_list2 = []
ok_list3 = []

num = 0

for linef, linefp in zip(f,fp):
    linef = linef.decode('utf-8').strip()
    linefp = linefp.decode('utf-8').strip()
    sf = perplexity_score(linef, model, ngram_num)
    sfp = perplexity_score(linefp, model, ngram_num)
    s2s_simple_p_list.append(sf)
    s2s_pos_p_list.append(sfp)
    if sf > sfp:
        ok_list1.append(sf)
        ok_list2.append(sfp)
        ok_list3.append(num)
    num += 1

cPickle.dump(ok_list3, open(r'ok-list.pkl', 'wb'))




assert len(s2s_simple_p_list) == len(s2s_pos_p_list)
assert len(s2s_pos_p_list) == 100

print "s2s perplexity is ", math.fsum(s2s_simple_p_list)/100.0
print "s2s pos perplexity is ", math.fsum(s2s_pos_p_list)/100.0

print len(ok_list3)


f.close()
fp.close()



# f = open(r'nba2-0.03.output')
# fp = open(r'POS-nba2-0.122.output')

# s2s_l = []
# s2s_p_l = []

# for linef, linefp in zip(f,fp):
#     linef = linef.decode('utf-8').strip()
#     linefp = linefp.decode('utf-8').strip()
#     lfl = list(ngrams(linef, ngram_num, pad_left=True, pad_right=True, left_pad_symbol='<s>', right_pad_symbol='</s>'))
#     lflp = list(ngrams(linefp, ngram_num, pad_left=True, pad_right=True, left_pad_symbol='<s>', right_pad_symbol='</s>'))
#     s2s_l += lfl
#     s2s_p_l += lflp



# f.close()
# fp.close()

# perp = 1
# N = 0
# for word in s2s_l:
#     N += 1
#     perp = perp * (1/model[word])
# perp = pow(perp, 1/float(N))

# print "s2s perplexity is ", perp

# perp = 1
# N = 0
# for word in s2s_p_l:
#     N += 1
#     perp = perp * (1/model[word])
# perp = pow(perp, 1/float(N))

# print "s2s pos perplexity is ", perp