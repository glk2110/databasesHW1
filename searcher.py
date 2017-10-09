#!/usr/bin/env python
#MAKE SURE TO DOWNLOAD NLTK AND nltk.download('punkt')

import pprint
import sys
import nltk

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

def getNewQuery(oldQuery, yWords, nWords):
	allWords = []
	realWords = []
	stopWords = ["a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"]
	for word in yWords:
		allWords.append(word)
	for word2 in nWords:
		allWords.append(word2)
	for string in allWords:
		tokens = nltk.word_tokenize(string.encode('utf-8'))
		for word3 in tokens:
			word3 = word3.lower()
			if word3 not in stopWords:
				realWords.append(word3)
	print(realWords)
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
	relevants = []
	relevantWords = []
	badWords = []
	for i in range(10):
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
		if good:
			if good[0] == "y" or good[0] == "Y":
				relevantWords.append(title)
				relevantWords.append(summary)
			else:
				badWords.append(title)
				badWords.append(summary)
		else:
			badWords.append(title)
			badWords.append(summary)
	printedFeedback = printFeedback(search, float(precision), relevants)
	if printedFeedback == 0:
		print("Still below the desired precision of " + str(float(precision)) + "\nExpanding Query\n")
		newSearch = getNewQuery(search, relevantWords, badWords)
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
