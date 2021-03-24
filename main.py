import requests
from bs4 import BeautifulSoup
total_topics_fetched=0
ch=input("do you want to enter sanfoundry site manually (yes/y/no/n) ?").lower()
fetchall=input("do you want to fetch all next mcq (yes/y/no/n) ?").lower()#fetch specific page or list of pages

if(ch=="yes" or ch=='y'):
    next_link=input().strip()
else:
    next_link="https://www.sanfoundry.com/computer-networks-mcqs-basics/" #sample site added

try:
    while True:
        data=requests.get(next_link)
        soup=BeautifulSoup(data.content,'html5lib')
        topic=soup.find('h1',attrs={'class':'entry-title'})
        print("Topic is",topic.text)
        #print(soup.prettify())
        list_of_div=soup.find('div',attrs={'class':'entry-content'})
        #print(len(list_of_div))
        #questions
        questions=list_of_div.findAll('p')[1:-3]
        #print(questions)
        questions_total=len(questions)
        print("total q ",questions_total)
        '''for q in questions:
            print(q.text)'''

        list_of_ans=soup.findAll('span',attrs={'class':'collapseomatic'})

        #answers
        list_of_ans=soup.findAll('div',attrs={'class':'collapseomatic_content'})[:questions_total]
        print(len(list_of_ans))

        '''for i in list_of_ans:
            print(i)'''

        for i in range(questions_total):
            print(questions[i].text)
            print(list_of_ans[i].text)

        #increment topic fetched counter
        total_topics_fetched+=1
        if(fetchall=='no' or fetchall=='n'):
            break
        links=soup.findAll('div',attrs={'class':'sf-nav-bottom'})
        next_link_a=links[1]
        #print(next_link)
        link_tag=next_link_a.find('a')
        print(link_tag)
        if(link_tag is None):
            print("End")
            break
        if('Next' in link_tag.text):#next link found
            next_link=link_tag['href']
            print(next_link)
            #break
        else:
            print("End")
            break

            
    print("Total topics fetched",str(total_topics_fetched))
except requests.exceptions.ConnectionError:
    print("Network Error")
