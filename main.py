import requests
from bs4 import BeautifulSoup
import os
import sys
total_topics_fetched=0
total_question_fetched=0

error_question=dict()

ch=input("do you want to enter sanfoundry site manually (yes/y/no/n) ?").lower()
fetchall=input("do you want to fetch all next topics to this (yes/y/no/n) ?").lower()#fetch specific page or list of pages

if(ch=="yes" or ch=='y'):
    next_link=input("enter site ").strip()
else:
    next_link="https://www.sanfoundry.com/computer-networks-mcqs-basics/" #sample site added

try:
    if('mcq.txt' in os.listdir()):
        print("already exists file with filename mcq.txt. Try renaming/deleting that file first")
        sys.exit()
    f=open('mcq.txt','wb')
    
    while True:
        data=requests.get(next_link)
        soup=BeautifulSoup(data.content,'html5lib')
        topic=soup.find('h1',attrs={'class':'entry-title'})
        if(topic is None):
            print("something went wrong")
            break
        heading=topic.text
        print("Topic:",heading)
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

        '''for i in list_of_ans:
            print(i)'''
        
        f.write("\n\n\t\t".encode()+heading.encode()+'\n\n'.encode())
        print(heading)
        for i in range(questions_total):
            total_question_fetched+=1
            currQuestion=questions[i].text
            currAns=list_of_ans[i].text
            #print(currQuestion,currAns)
            f.write(currQuestion.encode()+'\n'.encode()+currAns.encode()+'\n\n'.encode())
            #print(currQuestion)
            #print(currAns)

        #increment topic fetched counter
        total_topics_fetched+=1
        if(fetchall=='no' or fetchall=='n'):
            break
        links=soup.findAll('div',attrs={'class':'sf-nav-bottom'})
        next_link_a=links[1]
        #print(next_link)
        link_tag=next_link_a.find('a')
        #print(link_tag)
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

            
    print(f'Total topics fetched are {total_topics_fetched} with total questions {total_question_fetched}')

except requests.exceptions.ConnectionError:
    print("Network Error")
