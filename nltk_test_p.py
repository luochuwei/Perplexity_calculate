corpus ="""
Monty Python (sometimes known as The Pythons) were a British surreal comedy group who created the sketch comedy show Monty Python's Flying Circus,that first aired on the BBC on October 5, 1969. Forty-five episodes were made over four series. The Python phenomenon developed from the television series into something larger in scope and impact, spawning touring stage shows, films, numerous albums, several books, and a stage musical.The group's influence on comedy has been compared to The Beatles' influence on music."""

import collections, nltk
# we first tokenize the text corpus
tokens = nltk.word_tokenize(corpus)

#here you construct the unigram language model 
def unigram(tokens_for_unigram):    
    model = collections.defaultdict(lambda: 0.01)
    for f in tokens_for_unigram:
        try:
            model[f] += 1
        except KeyError:
            model [f] = 1
            continue
    for word in model:
        model[word] = model[word]/float(len(model))
    return model


#computes perplexity of the unigram model on a testset  
def perplexity(testset, model):
    testset = testset.split()
    perplexity = 1
    N = 0
    for word in testset:
        N += 1
        perplexity = perplexity * (1/model[word])
    perplexity = pow(perplexity, 1/float(N)) 
    return perplexity


testset1 = "Monty"
testset2 = "abracadabra gobbledygook rubbish"

model = unigram(tokens)
print perplexity(testset1, model)
print perplexity(testset2, model)


# from nltk.util import ngrams

# def ngram_for_model(tokens_for_ngram, n):
#     model = collections.defaultdict(lambda: 0.01)
#     for f in ngrams(tokens_for_ngram, n):
#         try:
#             model[f] += 1
#         except KeyError:
#             model [f] = 1
#             continue
#     for word in model:
#         model[word] = model[word]/float(len(model))
#     return model


# # testset1 = "Monty"
# # testset2 = "abracadabra gobbledygook rubbish"


# def perplexity2(testset, model, n):
#     testset = testset.split()
#     perplexity = 1
#     N = 0
#     for word in ngrams(testset, n):
#         N += 1
#         perplexity = perplexity * (1/model[word])
#     perplexity = pow(perplexity, 1/float(N)) 
#     return perplexity


# ngram_for_test = 1
# m = ngram_for_model(tokens, ngram_for_test)
# print perplexity2(testset1, m, ngram_for_test)
# print perplexity2(testset2, m, ngram_for_test)




# testset3 = "a British happy comedy group"
# testset4 = "Python and music"

# ngram_for_test = 2
# m = ngram_for_model(tokens, ngram_for_test)
# print perplexity2(testset3, m, ngram_for_test)
# print perplexity2(testset4, m, ngram_for_test)
