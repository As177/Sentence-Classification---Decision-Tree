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

File = open("train.txt","r")
trainData = File.read()
trainText = trainData.split("\n")
trainText.pop()

trainFile = open("train.arff","w")


bigrams = Counter()
trigrams = Counter()
#######creating classes array###########333
classes=[]
train_data_file = open("train_data.txt","r")
data = train_data_file.read()
lines = data.split("\n")
lines.pop()
for line in lines:
	token = line.split(":")
	classes.append(token[0])
# print "classes: "+str(len(classes))
# print "train.txt : "+str(len(trainText))

########## writing training file ###########
deleteContent(trainFile)
trainFile.write("@RELATION classification_questions\n\n")

for x in range(1,1501):
	trainFile.write("@ATTRIBUTE attribute{0}  ".format(x))
	trainFile.write("{0,1}\n")
trainFile.write("@ATTRIBUTE class {DESC, ENTY, ABBR, HUM, NUM, LOC}\n")
trainFile.write("@DATA\n")
count =0

for line in trainText:
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
			trainFile.write("1,")
		else:
			trainFile.write("0,")
	##printing class for each line
	#print text
	#print "count: ",count
	trainFile.write("{0}\n".format(classes[count]))
	count+=1

