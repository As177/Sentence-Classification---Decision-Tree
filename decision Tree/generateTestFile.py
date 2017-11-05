import nltk
from nltk import word_tokenize
from nltk.util import ngrams
from nltk.corpus import stopwords
from collections import Counter
import heapq
import re
import string
import sys

def deleteContent(pfile):
    pfile.seek(0)
    pfile.truncate()
##### generating vocabulary ########
vocabfile=open("vocabulary.txt")
data = vocabfile.read()
lines = data.split("\n")
lines.pop()
vocab = []
for line in lines:
	tokens = line.split(" ")
	vocab.append("{0}".format(tokens[0]))
print "length of vocab : "+str(len(vocab))
####################################################

File = open("test.txt","r")
testData = File.read()
testText = testData.split("\n")
testText.pop()


testFile  = open("test.arff","w")

bigrams = Counter()
trigrams = Counter()
#######creating classes array###########333
classes=[]
test_data_file = open("test_data.txt","r")
data = test_data_file.read()
lines = data.split("\n")
lines.pop()
for line in lines:
	token = line.split(":")
	classes.append(token[0])
# print "classes: "+str(len(classes))
# print "test.txt : "+str(len(testText))

########## writing testing file ###########
deleteContent(testFile)
testFile.write("@RELATION classification_questions\n\n")

for x in range(1,1501):
	testFile.write("@ATTRIBUTE attribute{0}  ".format(x))
	testFile.write("{0,1}\n")
testFile.write("@ATTRIBUTE class {DESC, ENTY, ABBR, HUM, NUM, LOC}\n")
testFile.write("@DATA\n")
count =0

for line in testText:
	text =[]
	unigrams=nltk.word_tokenize(line)
	for x in unigrams:
		text.append("{0}".format(x))
	bi = ngrams(unigrams,2)
	bigrams.update(bi)
	tri = ngrams(unigrams,3)
	trigrams.update(tri)
	for x in bigrams.keys():
		text.append("{0}-{1}".format(x[0],x[1]))
	for x in trigrams.keys():
		text.append("{0}-{1}-{2}".format(x[0],x[1],x[2]))

	for x in vocab:
		if x in text:
			testFile.write("1,")
		else:
			testFile.write("0,")
	##printing class for each line
	#print text
	#print "count: ",count
	testFile.write("{0}\n".format(classes[count]))
	count+=1

