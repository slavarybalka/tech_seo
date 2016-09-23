#Python 2.7

import requests
from requests.exceptions import ConnectionError
import csv
from BeautifulSoup import BeautifulSoup


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
	
	#check if sitemap.xml or index_sitemap.xml are on the site
	#count the URLs in the sitemap
    

def analyze_sitemap_links(sitemap):
	# this function takes body of the sitemap as an input and outputs 2 things:
	# a list of URLs from the sitemap
	# the number of URLs in the list
    links_in_sitemap = []
    soup = BeautifulSoup(sitemap)

    for url in soup.findAll("loc"):
        #print url.text
        links_in_sitemap.append(url.text)
    #scan the URLs
    
    return links_in_sitemap, len(links_in_sitemap)
    

def get_time_to_first_byte(webpage):
	#already completed, paste the code
    pass   




############### EXECUTION #################

with open('our_sites.txt') as f:
    list_of_our_sites = f.read().splitlines()


export_list = []

for website in list_of_our_sites:
    print '\nWebsite: ', website
    mobile_data = check_mobile_speed_usability(website)  # checking mobile page speed and optimization
    robots = get_robots_txt(website)                     # checking if robots.txt is present on the site
    sitemap_xml = get_sitemap(website)[0]                # returns the status code of the sitemap
    sitemap_contents = get_sitemap(website)[1]           # body of the sitemap
    links_in_sitemap = analyze_sitemap_links(sitemap_contents)

    print 'Mobile Page Speed: ', mobile_data[0] 
    print 'Mobile Usability Score: ', mobile_data[1]
    print 'robots.txt: ', robots
    print 'sitemap.xml: ', sitemap_xml
    print 'Links in sitemap: ', links_in_sitemap[1]

    export_list.append([website, mobile_data[0], mobile_data[1], robots, sitemap_xml, links_in_sitemap[1]])

with open('eggs.csv', 'wb') as csvfile:
    seowriter = csv.writer(csvfile, delimiter=',')
    seowriter.writerow(['Website','Page Speed - Mobile','Mobile Usability Score','Robots.txt','Sitemap.xml', 'Links in sitemap']) #writing headers
    for website_data in export_list:
        seowriter.writerow(website_data)

