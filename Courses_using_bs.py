from bs4 import BeautifulSoup
from urllib.request import urlopen


def college_BE_course(link):
    sauce=urlopen(link).read()
    soup = BeautifulSoup(sauce ,"lxml")
    try:
        list1=[]
        college_courses_container=soup.find("div", class_="div-stream-list")
        course_list=college_courses_container.find_all("a")
        for course in course_list:
            list1.append(course.text)
        return list1
    except:
        return None

def college_fee_overview(link):
    sauce=urlopen(link).read()
    soup = BeautifulSoup(sauce ,"lxml")
    college_fees_list=soup.find("tbody")
    try:
        fees_list=college_fees_list.find("tr")
        fees=fees_list.find_all("td")
        #FE,SE,TE,BE,TotalFeee
        return fees[0],fees[1],fees[2],fees[3],fees[4]
    except:
        return None,None,None,None,None
