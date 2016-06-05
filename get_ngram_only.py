#-*- coding:utf-8 -*-

import re
import cPickle
import jieba
import time

import collections, nltk

from nltk.util import ngrams

def ngram_return_model(model, tokens_for_ngram, n):
    for f in ngrams(tokens_for_ngram, n):
        try:
            model[f] += 1
        except KeyError:
            model [f] = 1
            continue
    return model




def perplexity_score(testset, model, n):
    testset = "<s> " + testset + " <s>"
    testset = testset.split()
    perplexity = 1
    N = 0
    for word in ngrams(testset, n):
        N += 1
        perplexity = perplexity * (1/model[word])
    perplexity = pow(perplexity, 1/float(N)) 
    return perplexity




pid_p_r_seg = cPickle.load(open(r'pid_p_r_seg-0604.pkl', 'rb'))


# a = pid_p_r[0][0]

# b = find_all_url(a, replace_urls=1)

# c = ' '.join(jieba.cut(b))

# d = delete_mark(c)

ngram_num = 3
model = collections.defaultdict(lambda: 0.01)

print "training ",ngram_num," model..."
for pid in pid_p_r_seg:
    in_start = time.time()
    
    post_seg = pid_p_r_seg[pid][0]
    post_seg_for_ngram = "<s> "+post_seg+" <s>"
    model = ngram_return_model(model, post_seg_for_ngram.split(), ngram_num)
    for r_seg in pid_p_r_seg[pid][1]:
        r_seg_for_ngram = "<s> "+r_seg+" <s>"
        model = ngram_return_model(model, r_seg_for_ngram.split(), ngram_num)
    in_time = time.time() - in_start
    print "id : ", pid, "  Time : ", in_time


for word in model:
    model[word] = model[word]/float(len(model))

cPickle.dump(model, open(r'trigram.model', 'wb'))