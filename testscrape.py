import urllib2
from bs4 import BeautifulSoup
import re

# Ask user to enter URL
url = "http://www.nytimes.com/2014/03/10/world/asia/malaysia-airlines-flight.html?ref=world&_r=1"

# Open txt document for output
txt = open('ctp_output.txt', 'w')

# Parse HTML of article, aka making soup
soup = BeautifulSoup(urllib2.urlopen(url).read())

# Write the article title to the file    
title = soup.find("h1")
txt.write('\n' + "Title: " + title.string + '\n' + '\n')

# Write the article date to the file    
try:
    date = soup.find("span", {'class':'dateline'}).text
    txt.write("Date: " + str(date) + '\n' + '\n')
except:
    print "Could not find the date!"

# Write the article author to the file    
try:
    byline=soup.find("p", {'class':'byline-author'}).text
    txt.write("Author: " + str(byline) + '\n' + '\n')
except:
    print "Could not find the author!"

# Write the article location to the file    
regex = '<span class="location">(.+?)</span>'
pattern = re.compile(regex)
byline = re.findall(pattern,str(soup))
txt.write("Location: " + str(byline) + '\n' + '\n')

# retrieve all of the paragraph tags
with open('ctp_output.txt', 'w'):
    for tag in soup.find_all('p'):
        txt.write(tag.text.encode('utf-8') + '\n' + '\n')

# Close txt file with new content added
txt.close()