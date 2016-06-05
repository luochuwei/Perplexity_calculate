#-*- coding:utf-8 -*-

import re
import cPickle
import jieba

def delete_mark(sentence):
    mark_list = [u'﹃', u'』',u'『', u'。', u'.', u'!', u'！', u'?', u'？', u'；', u';',u'~',u'～',u'(', u')', u'（', u'）', u'-',u'+',u'=',u'、', u'》', u'《', u'，', u'】', u'【', u'̩̩̩̩̩̩̩…', u'•', u'＂', u'—', u'＄', u'¤', u'∩', u'_', u'“', u'”', u'«', u'»', u'‘', u'’', u'[', u']', u'{', u'}', u'`', u'^', u':', u'：',u'|', u'︶',u'︿', u'▄', u'︻', u'┳', u'═', u'┢', u'┦', u'Ρ', u'ｐ', u'≧',u'≦', u'﹏', u'_', u'@', u'︿', u'￣', u'︶', u'︽', u'╭' ,u'∩' ,u'╮', u'﹊', u'↘', u'┬', u'↗', u'∠', u'※', u'ε', u'┻', u'▇', u'●', u'○', u'▽', u'０', u'︼', u'★', u'┈', u'━', u'☆', u'ψ', u'╰', u'╯', u'‵', u'′', u'ｏ', u'⊙', u'└', u'┘', u'∞', u'≡', u'◎', u'◑', u'→', u'∵', u'ˇ']
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


a = pid_p_r[0][0]

b = find_all_url(a, replace_urls=1)

c = ' '.join(jieba.cut(b))

d = delete_mark(c)