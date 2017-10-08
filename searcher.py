#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Simple command-line example for Custom Search.
Command-line application that does a search.
"""


import pprint
import sys

from googleapiclient.discovery import build

def printFeedback(query, precision, relevants):
	realPrecision = 0.0
	for elem in relevants:
		if elem[0] == "y" or elem[0] == "Y":
			realPrecision = realPrecision + .1
	print("======================")
	print("FEEDBACK SUMMARY")
	print("Query: ")
	print("Precision: " + realPrecision)
	if precision > realPrecision:
		return False
	return True

def expandQuery():
	print("expanding query")

def main():
	# Build a service object for interacting with the API. Visit
	# the Google APIs Console <http://code.google.com/apis/console>
	# to get an API key for your own application.
	apiKey = sys.argv[1]
	engineID = sys.argv[2]
	precision = sys.argv[3]
	search = sys.argv[4]
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
	for i in range(10):
		print("Result " + str(i + 1) + "\n")
		solution = str(res[u'items'][i][u'link'])
		title =  str(res[u'items'][i][u'title'])
		print(" URL: " +solution)
		print(" Title: "+ title)
		summary = res[u'items'][i][u'snippet']
		print(" Summary: " + summary)
		print("\nIs this Relevant (Y/N)?")
		relevants.append(raw_input())
	if printFeedback(query, precision, relevants) == False:
		print("Still below the desired precision of " + str(precision))
		expandQuery()
	else:
		print("Desired precision reached, done")

if __name__ == '__main__':
	main()
