#dependencies
import operator
import json
from tabulate import tabulate
import sys
from functions import *	# all functions reside in this file


#get data from wiki
wikipedia_api_link = 	"http://en.wikipedia.org/w/api.php?action=query&format=json&list=search&srsearch="
wikipedia_link = "http://en.wikipedia.org/wiki/"

if(len(sys.argv) < 2):
	print("Enter a valid string")
	exit()

#get search word
string_query = sys.argv[1]	#python3 main.py batman yes|no <-- argv[1]

if(len(sys.argv) > 2):
	search_mode = True
else:
	search_mode = False

#create url
url = wikipedia_api_link + string_query
try:
	response = requests.get(url)
	data = json.loads(response.content.decode('utf-8'))
	#format data

	page_word_list = []
	print("Scrapping Wikipedia pages..")
	search_result = data['query']['search']
	if(len(search_result) < 1):
		print("No search result, try checking the spelling.")
	for i in range(len(search_result)):
		wikipedia_page_tag = search_result[i]['title']
		#create new url
		url = wikipedia_link + wikipedia_page_tag
		page_word_list.extend(getWordList(url) + wikipedia_page_tag.split()) # getWordList(url) --> Takes url and scrap all the words from <p> tags of page.
		print(url)

	#create table of word counts
	page_word_counts = createFrequencyTable(page_word_list)
	sorted_word_frequency_list = sorted(page_word_counts.items(), key=operator.itemgetter(1), reverse=True)
	
	#remove stop words
	if(search_mode):
		sorted_word_frequency_list = remove_stop_words(sorted_word_frequency_list)
	
	#sum total words to calcalate frequencies
	total_words_sum = 0
	for key, value in sorted_word_frequency_list:
		total_words_sum += value

	#just get top 20 words
	if len(sorted_word_frequency_list) > 20:
		sorted_word_frequency_list = sorted_word_frequency_list[:20]
	print("\nTop 20 words related to {}.\n".format(string_query))

	#create our final list, words + frequency + percentage
	final_list = []
	for key, value in sorted_word_frequency_list:
		percentage_value = float(value*100) / total_words_sum
		final_list.append([key, value, round(percentage_value, 4)])

	print_headers = ['Word', 'Frequency', 'Frequency Percentage']

	#print the table with tabulate
	print(tabulate(final_list, headers=print_headers, tablefmt='orgtbl'))

#throw an exception in case it breaks
except requests.exceptions.Timeout:
    print("The server didn't respond. Please, try again later.")
