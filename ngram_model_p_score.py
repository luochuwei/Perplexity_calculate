#-*- coding:utf-8 -*-
####################################################
#
#    Author: Chuwei Luo
#    Email: luochuwei@gmail.com
#    Date: 21/02/2016
#    Usage: new Main (in case of the out of memory)
#
####################################################

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
        # print perplexity
    perplexity = pow(perplexity, 1/float(N)) 
    return perplexity




f = open(r'corpus.txt')

corpus_dic = {}

for num, line in enumerate(f):
    line = "<s> "+line.strip()+" <s>"
    print line.decode('utf-8')
    corpus_dic[num] = line.split()
f.close()

#build ngram model
ngram_num = 3
model = collections.defaultdict(lambda: 0.01)
# model = {}
for num in corpus_dic:

    for f in ngrams(corpus_dic[num], ngram_num):
        if f in model:
            model[f] += 1
        else:
            model[f] = 1

for word in model:
    model[word] = model[word]/float(len(model))





testset1 = "你 是 天气 的 了"
testset2 = "我 想 看 球 了"

print perplexity_score(testset1, model, ngram_num)
print perplexity_score(testset2, model, ngram_num)
