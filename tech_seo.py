#Python 2.7

import requests
from requests.exceptions import ConnectionError
import csv
from BeautifulSoup import BeautifulSoup
import re
import time
import urllib2


############## SETUP #################

def check_mobile_speed_usability(webpage):

	m = requests.get('https://www.googleapis.com/pagespeedonline/v2/runPagespeed?url=http%3A%2F%2F'+website+'&strategy=mobile')
	mobile_data = m.json()
	return [mobile_data['ruleGroups']['SPEED']['score'], mobile_data['ruleGroups']['USABILITY']['score']]
	

def get_robots_txt(webpage):
	
	try:
	    r = requests.get('http://' + website + '/robots.txt')
	    robots = r.status_code
	    print robots
	except ConnectionError as e:    # This is the correct syntax
	    robots = "No response"
        print robots

	return robots
	
	#check if robots.txt is on the site
	

def get_sitemap(webpage):
	try:
		s = requests.get('http://' + website + '/sitemap.xml')
		sitemap_status_code = s.status_code
		sitemap_body = s.text

	except ConnectionError as e:	
		sitemap_body = "Connection Error"
		sitemap_status_code = "Connection Error"
	return sitemap_status_code, sitemap_body
	
	# check if sitemap.xml or index_sitemap.xml are on the site
	# count the URLs in the sitemap
    

def analyze_sitemap_links(sitemap):
	# this function takes body of the sitemap as an input and outputs 2 things:
	# a list of URLs from the sitemap
	# the number of URLs in the list
    links_in_sitemap = []
    soup = BeautifulSoup(sitemap)

    for url in soup.findAll("loc"):
        # print url.text
        links_in_sitemap.append(url.text)
    # scan the URLs
    
    return links_in_sitemap, len(links_in_sitemap)
    

def get_time_to_first_byte(webpage):
    try:
        start = time.time()
        f = urllib2.urlopen('http://' + website)
        f.read(1)
        end = time.time() 
        ttfb = round(end - start, 3)

    except ConnectionError as e:    # This is the correct syntax
        ttfb = "some error occured"
    
    return str(ttfb)
    

def pages_in_google_index(webpage):
    # google site:website and return the number of pages
    google_query = requests.get('https://www.google.com/search?num=10&ion=1&espv=&ie=UTF-8&q=site%3A' + website)
    result = google_query.text
    code = google_query.status_code
    print code
    #print result
    try:
        output = re.findall('resultStats">(About\s)?([\d]+)', result)
    
        x = output[0][1]
    except:
        x = 0
    return x


def sitemap_urls_to_indexed_ratio(sitemap_links, indexed_links):
    try:
        ratio = indexed_links / sitemap_links
    except ZeroDivisionError:
        ratio = 0
    return ratio

############### EXECUTION #################

with open('our_sites.txt') as f:
    list_of_our_sites = f.read().splitlines()

#list_of_our_sites = ['degree.astate.edu', 'online.uakron.edu','micampus.fucsalud.edu.co']

export_list = []

for website in list_of_our_sites:
    print '\nWebsite: ', website
    mobile_data = check_mobile_speed_usability(website)        # checking mobile page speed and optimization
    robots = get_robots_txt(website)                           # checking if robots.txt is present on the site
    sitemap_xml = get_sitemap(website)[0]                      # returns the status code of the sitemap
    sitemap_contents = get_sitemap(website)[1]                 # body of the sitemap
    links_in_sitemap = analyze_sitemap_links(sitemap_contents) # check the links in the sitemap
    google_search_results = pages_in_google_index(website)      # get number of pages indexed in Google
    url_indexing_ratio = sitemap_urls_to_indexed_ratio(float(links_in_sitemap[1]), float(google_search_results))
    uir = round(url_indexing_ratio, 3) * 100
    ttfb = get_time_to_first_byte(website)

    print 'Mobile Page Speed: ', mobile_data[0] 
    print 'Mobile Usability Score: ', mobile_data[1]
    print 'robots.txt: ', robots
    print 'sitemap.xml: ', sitemap_xml
    print 'Links in sitemap: ', links_in_sitemap[1]
    print 'Pages in Google Index', google_search_results
    print 'URL indexing ratio', uir
    print 'Time to first byte', ttfb

    export_list.append([website, mobile_data[0], mobile_data[1], robots, sitemap_xml, links_in_sitemap[1], google_search_results, str(uir)+'%', ttfb])

with open('tech_seo_results.csv', 'wb') as csvfile:
    seowriter = csv.writer(csvfile, delimiter=',')
    seowriter.writerow(['Website','Page Speed - Mobile','Mobile Usability Score','Robots.txt','Sitemap.xml', 'URLs in sitemap', 'URLs in Google', 'Indexing Ratio', 'Time to First Byte']) #writing headers
    for website_data in export_list:
        seowriter.writerow(website_data)





