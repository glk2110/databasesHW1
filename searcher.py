#!/usr/bin/env python
#MAKE SURE TO DOWNLOAD NLTK AND nltk.download('punkt')

import pprint
import sys
import nltk
import string

from googleapiclient.discovery import build

def printFeedback(query, precision, relevants):
	realPrecision = .0
	for elem in relevants:
		if elem:
			if elem[0] == "y" or elem[0] == "Y":
				realPrecision = realPrecision + .1
	print("======================")
	print("FEEDBACK SUMMARY")
	print("Query: " + query)
	print("Precision: " + str(realPrecision))
	if realPrecision == .0:
		return 2
	elif precision > realPrecision:
		return 0
	return 1

def getNewQuery(oldQuery, allWords):
	realWords = []
	stopWords = ["a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"]
	for string2 in allWords:
		realWords1 = []
		for string1 in string2:
			exclude = set(string.punctuation)
			temp = ''.join(ch for ch in string1 if ch not in exclude)
			tokens = nltk.word_tokenize(temp)
			for word3 in tokens:
				word3 = word3.lower()
				if word3 not in stopWords:
					if word3 != "":
						realWords1.append(word3)
		realWords.append(realWords1)
	wordList = []
	for i in realWords:
		for j in i:
			if j not in wordList:
				wordList.append(j)
	termFrequency = {}
	art = 10
	for word4 in wordList:
		termFrequency[word4] = []
		art = art - 10
		for article in realWords:
			countWord = 0
			for word5 in article:
				if word5==word4:
					countWord += 1
			art = art + 1
			termFrequency[word4].append([art,countWord])
	tfidf = {}
	for word6 in wordList:
		cnt = 0
		for article1 in realWords:
			tf = termFrequency[word6][cnt][1]/len(realWords[cnt])
			print(tf)
			cnt = cnt + 1
	return oldQuery

def makeQuery(apiKey, engineID, precision, search):
	service = build("customsearch", "v1",
		developerKey=apiKey)

	res = service.cse().list(
		q=search,
		cx=engineID,
	).execute()

	print("Parameters:")
	print("Client Key	= " + apiKey)
	print("Engine Key 	= " + engineID)
	print("Query		= " + search)
	print("Precision 	= " + str(precision))
	print("Google Search Results:")
	print("======================")
	global relevants
	relevants = []
	relevantWords = []
	badWords = []
	for i in range(10):
		temp = []
		print("Result " + str(i + 1) + "\n")
		solution = str(res[u'items'][i][u'link'])
		title =  str(res[u'items'][i][u'title'])
		print(" URL: " +solution)
		print(" Title: "+ title)
		summary = res[u'items'][i][u'snippet']
		print(" Summary: " + summary)
		print("\nIs this Relevant (Y/N)?")
		good = raw_input()
		relevants.append(good)
		temp.append(title)
		temp.append(summary.encode('ascii','ignore'))
		relevantWords.append(temp)
	printedFeedback = printFeedback(search, float(precision), relevants)
	if printedFeedback == 0:
		print("Still below the desired precision of " + str(float(precision)) + "\nExpanding Query\n")
		newSearch = getNewQuery(search, relevantWords)
		makeQuery(apiKey, engineID, precision, newSearch)
	elif printedFeedback == 1:
		print("Desired precision reached, done")
	else:
		print("Below desired precision but can no longer augment the query")
def main():
	# Build a service object for interacting with the API. Visit
	# the Google APIs Console <http://code.google.com/apis/console>
	# to get an API key for your own application.
	apiKey = sys.argv[1]
	engineID = sys.argv[2]
	precision = sys.argv[3]
	search = sys.argv[4]
	makeQuery(apiKey, engineID, precision, search)

if __name__ == '__main__':
	main()
