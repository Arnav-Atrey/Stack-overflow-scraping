import requests
import urllib.parse
import csv
import pandas as pd
from bs4 import BeautifulSoup as bs

def make_file(URL,x):
    PAGE = requests.get(URL)
    data = []
    SOUP = bs(PAGE.content,"html.parser")
    
    question = SOUP.find_all('div', class_='s-prose js-post-body')[0]
    data.append("QUESTION: \n")
    for i in question:
        if i.name in ['p', 'pre']:
            data.append(i.get_text().strip().replace('\n','')) #needs work 
    total=SOUP.find_all('div',"js-vote-count flex--item d-flex fd-column ai-center fc-theme-body-font fw-bold fs-subheading py4")
    y=int(total[0].get_text())
    data.append('TOTAL NO OF UPVOTES: ')
    data.append(y)
    data.append('\n')    
    data.append("ANSWERS \n")

    acc=SOUP.find('div',id="answers").find_all('div',class_="answer js-answer accepted-answer js-accepted-answer")
    for a in acc:
        content = a.find_all('div', class_='s-prose js-post-body')
        for i in content:
            for element in i.contents:
                if element.name in ['p', 'pre']:
                    data.append(element.get_text().strip().replace('\n', ''))

        upvotes = a.find_all('div', class_='js-vote-count flex--item d-flex fd-column ai-center fc-black-500 fs-title')
        for j in upvotes:
            data.append('Upvotes recieved: ')
            data.append(j.get_text().strip().replace('\r\n            ', ''))
            data.append('THIS ANSWER WAS MARKED CORRECT BY THE USER')
            data.append('\n')

    n_acc=SOUP.find('div', id='answers').find_all('div', class_='answer js-answer')
    for a in n_acc:
        content = a.find_all('div', class_='s-prose js-post-body')
        for i in content:
            for element in i.contents:
                if element.name in ['p', 'pre']:
                    data.append(element.get_text().strip().replace('\n', ''))

        upvotes = a.find_all('div', class_='js-vote-count flex--item d-flex fd-column ai-center fc-black-500 fs-title')
        for j in upvotes:
            data.append('Upvotes recieved: ')
            data.append(j.get_text().strip().replace('\r\n            ', ''))
            data.append('\n')

    df = pd.DataFrame({x: data})

    # Export the DataFrame to an Excel file
    df.to_excel(f'output{x}.xlsx', index=False)  

def extraction(soup,x):
    url = "https://stackoverflow.com/"
    questions=soup.find('div',class_="js-post-summaries").find_all('a',class_="s-link")
    n=len(questions)
    for i in range(n):
        if x>1:
            make_file(url+str(questions[i]['data-searchsession']),i+1+(x-1)*n)
        else:
            make_file(url+str(questions[i]['data-searchsession']),i+1)
       
st=input("Enter tag to scrape: ")
url = "https://stackoverflow.com/"
search_url=url+'search?q='+urllib.parse.quote(st)
page = requests.get(search_url)
soup = bs(page.content,"html.parser")# prints the raw HTML Code
count=soup.find('div',class_='s-pagination site1 themed pager float-left').find_all('a','s-pagination--item js-pagination-item')
c=count[len(count)-2].get_text()
x=int(c)
print(x)
for i in range(1,3): # it should be x+1 instead of 3. it was made 3 as extracting data from x pages would take too long
    final_url=f"https://stackoverflow.com/search?page={i}&tab=Relevance&pagesize=15&q="+urllib.parse.quote(st)+"&searchOn=3"
    print(final_url)
    page = requests.get(final_url)
    #print(page.status_code)
    soup = bs(page.content,"html.parser")# prints the raw HTML Code
    extraction(soup,i)
    print("DONE",i)
