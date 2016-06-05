#-*- coding:utf-8 -*-

import re
import cPickle
import jieba


import collections, nltk

from nltk.util import ngrams

def ngram_return_model(model, tokens_for_ngram, n):
    for f in ngrams(tokens_for_ngram, n):
        try:
            model[f] += 1
        except KeyError:
            model [f] = 1
            continue
    for word in model:
        model[word] = model[word]/float(len(model))
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

def delete_mark(sentence):
    mark_list = [u'﹃', u'』',u'『', u'。', u'.', u'!', u'！', u'?', u'？', u'；', u';',u'~',u'～',u'(', u')', u'（', u'）', u'-',u'+',u'=',u'、', u'》', u'《', u'，', u'】', u'【', u'̩̩̩̩̩̩̩…', u'•', u'＂', u'—', u'＄', u'¤', u'∩', u'_', u'“', u'”', u'«', u'»', u'‘', u'’', u'[', u']', u'{', u'}', u'`', u'^', u':', u'：',u'|', u'︶',u'︿', u'▄', u'︻', u'┳', u'═', u'┢', u'┦', u'Ρ', u'ｐ', u'≧',u'≦', u'﹏', u'_', u'@', u'︿', u'￣', u'︶', u'︽', u'╭' ,u'∩' ,u'╮', u'﹊', u'↘', u'┬', u'↗', u'∠', u'※', u'ε', u'┻', u'▇', u'●', u'○', u'▽', u'０', u'︼', u'★', u'┈', u'━', u'☆', u'ψ', u'╰', u'╯', u'‵', u'′', u'ｏ', u'⊙', u'└', u'┘', u'∞', u'≡', u'◎', u'◑', u'→', u'∵', u'ˇ', u'\'', u'"', u'♪', u'ᴖ', u'◡', u'๑', u'〜', u'❤', u'ω']
    for i in mark_list:
        if i in sentence:
            sentence = sentence.replace(i, '')


    return sentence
def find_all_url(sentence, show_urls = None, replace_urls = None):
    r = re.compile(r'(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))')
    url_list = r.findall(sentence)
    if show_urls == 1:
        print "find", str(len(url_list)), "URLs"
        for i in url_list:
            print i[0]

    if replace_urls == 1:
        for j in url_list:
            sentence = sentence.replace(j[0], 'URL')
            # sentence = sentence.replace(j[0], '')
        return sentence
    return 1


pid_p_r = cPickle.load(open(r'pid_p_r.pkl', 'rb'))

pid_p_r_seg = {}
# a = pid_p_r[0][0]

# b = find_all_url(a, replace_urls=1)

# c = ' '.join(jieba.cut(b))

# d = delete_mark(c)

ngram_num = 3
model = collections.defaultdict(lambda: 0.01)

print "training ",ngram_num," model..."
for pid in pid_p_r:
    print pid
    post = find_all_url(pid_p_r[pid][0], replace_urls=1)
    post_seg = ' '.join(jieba.cut(post))  #jieba出来的是unicode
    post_seg = delete_mark(post_seg)
    pid_p_r_seg[pid] = [post_seg]
    # post_seg_for_ngram = "<s> "+post_seg+" <s>"
    # model = ngram_return_model(model, post_seg_for_ngram.split(), ngram_num)
    r_seg_list = []
    for response in pid_p_r[pid][1]:
        response = find_all_url(response, replace_urls=1)
        r_seg = ' '.join(jieba.cut(response))
        r_seg = delete_mark(r_seg)
        r_seg_list.append(r_seg)
        # r_seg_for_ngram = "<s> "+r_seg+" <s>"
        # model = ngram_return_model(model, r_seg_for_ngram.split(), ngram_num)
    pid_p_r_seg[pid].append(r_seg_list)



cPickle.dump(pid_p_r_seg, open(r'pid_p_r_seg.pkl', 'wb'))
cPickle.dump(model, open(r'trigram.model', 'wb'))