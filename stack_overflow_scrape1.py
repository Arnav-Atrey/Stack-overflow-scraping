import requests
import urllib.parse
import csv
from bs4 import BeautifulSoup as bs

url = "https://stackoverflow.com/"
page = requests.get(url)
# Prints the content on page:
# print(page.content)
print(page.status_code) #200 -> we can access data

st=input("Enter tag to scrape: ")
final_url=url+'search?q='+urllib.parse.quote(st)
print(final_url)
page = requests.get(final_url)
print(page.status_code)

soup = bs(page.content,"html.parser")  # prints the raw HTML Code
print(soup)

titles = soup.find('div',class_="js-post-summaries").find_all('h3',class_="s-post-summary--content-title")
for t in titles:
    ans=t.find('a',class_="s-link").get_text()
    print(ans) 
    
answers=soup.find('div',class_="js-post-summaries").find_all('span',class_="s-post-summary--stats-item-number")
for i in range(1,len(answers),3):
    ans=answers[i].get_text()
    votes=answers[i-1].get_text()
    print(ans, votes)