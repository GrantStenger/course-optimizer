"""
(c) 2019 - Grant Stenger
1/24/19 - Initial creation of Scraper
University of Southern California
"""

import requests
import os
from bs4 import BeautifulSoup

def main():

	# Create dirs if they do not exist
	if not os.path.exists('data/'):
		os.makedirs('data/')

	prefix = "MATH"
	page_number = 0
	url = "http://catalogue.usc.edu/content.php?filter%5B27%5D=" + prefix + \
		  "&filter%5B29%5D=&filter%5Bcourse_type%5D=-1&filter%5Bkeyword%5D=" + \
		  "&filter%5B32%5D=1&filter%5Bcpage%5D=" + str(page_number) + \
		  "&cur_cat_oid=8&expand=&navoid=2389" + \
		  "&search_database=Filter#acalog_template_course_filter"

	response = requests.get(url)
	soup = BeautifulSoup(response.text, "lxml")
	samples = soup.find("a").string.strip()

	print(samples)

	# opens file, pretty prints the JSON
	# with open("data/professors.json", 'w') as outfile:
	# 	final_data = data["response"]
	# 	final_data["ratings"] = final_data.pop("docs")
	# 	json.dump(final_data, outfile, indent=4)


if __name__ == "__main__":
	main()
