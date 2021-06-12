from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from urllib.request import urlopen
import time
from Courses_using_bs import college_BE_course
from Courses_using_bs import college_fee_overview
import csv

'''
from Courses_using_selenium import college_course
this will give more courses because we click SHOW MORE to show extra
courses dynamicaly. 
this package will take time because for each link browser open and close.'''

web_driver=webdriver.Chrome()
web_driver.get('https://collegedunia.com/engineering-colleges')
blocks = []
while len(blocks) < 40:
    blocks = web_driver.find_elements_by_class_name("listing-block")
    print(len(blocks))

    action = ActionChains(web_driver)
    action.move_to_element(blocks[len(blocks)-5])
    action.perform()

    try:
        close_popup = web_driver.find_element_by_class_name("close_modal_leadform")
        close_popup.click()
    except Exception as e:
        print("javascript popup will not appear.")
final=[]
for block in blocks:
    
    college_name = block.find_element_by_class_name("clg-name-address")
    
    
    location=block.find_element_by_class_name("location-badge")
    

    try:
        review_ratings= block.find_element_by_class_name("rating-text")
    except:
        print("Rating not Found")

    
    fee=  block.find_elements_by_class_name("lr-key")
    Be_first_year_fee=fee[0].text
    Me_first_year_fee=fee[0].text
    
    rank_list=[]
    if len(block.find_elements_by_class_name("rank-container")) >0:
        try:
            rank_containers=block.find_elements_by_class_name("rank-container")
            for rank_container in rank_containers:
                rank=rank_container.find_element_by_class_name("rank-span")
                name_of_authority=rank.find_element_by_tag_name("use")
                name_of_auth=name_of_authority.get_attribute("xlink:href")
                ranked=name_of_auth+rank.text
                rank_list.append(ranked)
                print(ranked)
                
        except Exception as e:
             print("error in rank")
    else:
        print("block is not Found")
    

    if len(block.find_elements_by_class_name("svg")) >0:
        try:
            avialibilities_list=[]
            avialibilities=block.find_elements_by_class_name("svg")
            for avialibility in avialibilities:
                avialibilities_list.append(avialibility.get_attribute("title"))
        except Exception as e:
            print("error in avialibility")
    else:
        avialibilities_list=None

    
    
    course_link = block.find_element_by_link_text("COURSES & FEES")
    course_list=college_BE_course(course_link.get_attribute('href'))
   
    

    first,second,third,fourth,overall=college_fee_overview(course_link.get_attribute('href'))
    if first is not None:
        first_year_fee=first.text
        second_year_fee=second.text
        third_year_fee=third.text
        fourth_year_fee=fourth.text
        overall_year_fee=overall.text
    else:
        first_year_fee=first
        second_year_fee=second
        third_year_fee=third
        fourth_year_fee=fourth
        overall_year_fee=overall
    
    
    last=(college_name.text,location.text,review_ratings.text,Be_first_year_fee,Me_first_year_fee,rank_list,avialibilities_list,course_list,first_year_fee,second_year_fee,third_year_fee,fourth_year_fee,overall_year_fee)
    final.append(last)
    
    
with open('Scraped_college_data.csv.csv', 'w',encoding='utf-8') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(final)
csvFile.close()    
time.sleep(5)
web_driver.close()
print("test complete")

'''
import pandas as pd
data=pd.read_csv("person.csv")
print(data.head())
'''
