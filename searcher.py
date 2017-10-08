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

	pprint.pprint("Parameters:")
	pprint.pprint("Client Key	=" + apiKey)
	pprint.pprint("Engine Key 	=" + engineID)
	pprint.pprint("Query		=" + search)
	pprint.pprint("Precision 	=" + precision)
	pprint.pprint("Google Search Results:")
	pprint.pprint("======================")
	relevants = []
	for i in range(10):
		pprint.pprint("Result " + i + "\n")
		solution = str(res[u'items'][i][u'link'])
		title =  str(res[u'items'][i][u'title'])
		pprint.pprint("URL: " +solution)
		pprint.pprint("Title: "+ title)
		summary = res[u'items'][i][u'snippet']
		pprint.pprint("Summary: " + summary)
		pprint.pprint("\nIs this Relevant (Y/N)?")

if __name__ == '__main__':
	main()
