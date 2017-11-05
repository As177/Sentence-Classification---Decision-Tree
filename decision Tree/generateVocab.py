import nltk
from nltk import word_tokenize
from nltk.util import ngrams
from nltk.corpus import stopwords
from collections import Counter
import heapq
import re
import string


def getGramsList(grams):
	return [(x,grams[x]) for x in grams.keys()]

def getTopNGrams(n,count,gramList):
	return heapq.nlargest(n, gramList, key=lambda s: s[count])

def deleteContent(pfile):
    pfile.seek(0)
    pfile.truncate()

def stripUnnecessary(s):
	s = s.translate(None, string.punctuation)
	stop_words = set(stopwords.words('english'))
	word_tokens = nltk.word_tokenize(s)
	filtered_sentence = ""
	for w in word_tokens:
	    if w not in stop_words:
	        filtered_sentence+=w+" "
	return filtered_sentence.strip()

#prepare training data

file =open('train_data.txt','r')
data = file.read()
trainingDataFile = open('train.txt','w')
deleteContent(trainingDataFile)
lines = data.split("\n")
lines.pop()

for line in lines:
	token = re.compile("[A-Z]+:[a-z]+ ").split(line)
	clean = stripUnnecessary(token[1])
	trainingDataFile.write(clean)
	trainingDataFile.write("\n")

#with open('train.txt', 'r') as myfile:
#   data=myfile.read().split()
unigrams = Counter()
bigrams = Counter()
trigrams = Counter()
tagsCounter = Counter()

tags=[]
posTags = []

for line in lines:
	token = re.compile("[A-Z]+:[a-z]+ ").split(line)
	clean = stripUnnecessary(token[1])
	tokens = nltk.word_tokenize(clean)
	unigrams.update(tokens)
	bi = ngrams(tokens,2)
	bigrams.update(bi)
	tri = ngrams(tokens,3)
	trigrams.update(tri)
	#nltk.pos_tag(tokens)
	for x in nltk.pos_tag(tokens):
	    tags.append(x)

for x in tags:
	posTags.append("{0}-{1}".format(x[0],x[1]))

tagsCounter.update(posTags)
tagsList = getGramsList(tagsCounter)
top500tags = getTopNGrams(500,1,tagsList)

#token = nltk.word_tokenize(text)

#unigrams = Counter(token)
UnigramList = getGramsList(unigrams)
top500unigrams = getTopNGrams(500,1,UnigramList)

#bi = ngrams(token,2)
#bigrams = Counter(bi)
bigramsList = getGramsList(bigrams)
top300bigrams = getTopNGrams(300,1,bigramsList)

#tri = ngrams(token,3)
#trigrams = Counter(tri)
trigramsList = getGramsList(trigrams)
top200trigrams = getTopNGrams(200,1,trigramsList)

#print the lists to file
vocabFile = open("vocabulary.txt",'w')
deleteContent(vocabFile)

for x in top500unigrams:
	vocabFile.write("{0} {1}".format(x[0],x[1]))
	vocabFile.write("\n")

for x in top300bigrams:
	vocabFile.write("{0}-{1} {2}".format(x[0][0],x[0][1],x[1]))
	vocabFile.write("\n")

for x in top200trigrams:
	vocabFile.write("{0}-{1}-{2} {3}".format(x[0][0],x[0][1],x[0][2],x[1]))
	vocabFile.write("\n")

for x in top500tags:
    vocabFile.write("{0} {1}".format(x[0],x[1]))
    vocabFile.write("\n")

#prepare testing data
file= open('test_data.txt','r')
data = file.read()
testingDataFile = open('test.txt','w')
deleteContent(testingDataFile)
lines = data.split("\n")
lines.pop()

for line in lines:
	token = re.compile("[A-Z]+:[a-z]+ ").split(line)
	clean = stripUnnecessary(token[1])
	testingDataFile.write(clean)
	testingDataFile.write("\n")
