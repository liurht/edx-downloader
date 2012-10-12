#!/usr/bin/env python
import os, pprint, sys, math, urllib,urllib2, cookielib, shutil, json , ClientCookie
from bs4 import BeautifulSoup
from datetime import timedelta, datetime

EDX_HOMEPAGE = 'https://www.edx.org'
LOGIN_API = 'https://www.edx.org/login'
DASHBOARD = 'https://www.edx.org/dashboard'
save_path = 'temp'
user_email = sys.argv[1]
user_pswd = sys.argv[2]

#Get Token
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
response = opener.open(EDX_HOMEPAGE)
set_cookie = {}
for cookie in cj:
    set_cookie[cookie.name] = cookie.value


#Prepare Headers

headers = {'User-Agent': 'edX-downloader/0.01',
           'Accept': 'application/json, text/javascript, */*; q=0.01',
           'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
           'Referer': EDX_HOMEPAGE,
           'X-Requested-With': 'XMLHttpRequest',
           'X-CSRFToken': set_cookie.get('csrftoken', '') }


#Login
post_data = urllib.urlencode({
            'email' : user_email,
            'password' : user_pswd,
            'remember' : False
            }).encode('utf-8')
request = urllib2.Request(LOGIN_API, post_data,headers)
response = urllib2.urlopen(request)
resp = json.loads(response.read().decode(encoding = 'utf-8'))
if not resp.get('success', False):
    print 'Wrong Email or Password.'
    exit(2)

#### Loged in - > saving cookies
c = ClientCookie.Cookies()
c.extract_cookies(response, request)

####Getting user info 
req = urllib2.Request(DASHBOARD,None,headers)
c.add_cookie_header(req)
resp = urllib2.urlopen(req)
#print resp.info()
dash = resp.read()
#print dash
soup = BeautifulSoup(dash)
data = soup.find_all('ul')[1]
USERNAME =  data.find_all('span')[1].string
USEREMAIL = data.find_all('span')[3].string
COURSES = soup.find_all('article')
courses = []
for COURSE in COURSES :
    c_name = COURSE.h3.string
    c_link = "https://www.edx.org"+COURSE.a['href']
    if c_link.endswith("info") or c_link.endswith("info/") :
        state = "Started"
    else :
        state = "Not yet"
    courses.append((c_name,c_link,state))
numOfCourses = len(courses)
print "Welcome " , USERNAME 
print "You can access ",numOfCourses," Courses on edX"
c = 0
for course in courses :
    c += 1
    print c, "- ",course[0]," -> ",course[2]
    
c_number = int(raw_input("Enter Course Number : "))
while c_number > numOfCourses or courses[c_number-1][2] != "Started" :
    print "Enter a valid Number for a Started Course ! between 1 and ",numOfCourses 
    c_number = int(raw_input("Enter Course Number : "))
exit(2)


########
links = []
links.append("https://www.edx.org/courses/BerkeleyX/CS188.1x/2012_Fall/courseware/Week_3/Lecture_4_CSPs")
links.append("https://www.edx.org/courses/BerkeleyX/CS188.1x/2012_Fall/courseware/Week_3/Lecture_4_CSPs_continued/")
links.append("https://www.edx.org/courses/BerkeleyX/CS188.1x/2012_Fall/courseware/Week_3/Lecture_5_CSPs_II/")
links.append("https://www.edx.org/courses/BerkeleyX/CS188.1x/2012_Fall/courseware/Week_3/Lecture_5_CSPs_II_continued/")

video_id = []
for link in links :
	req = urllib2.Request(link,None,headers)
	
	c.add_cookie_header(req)
	resp = urllib2.urlopen(req)

	page =  resp.read()

	id_container = page.split("data-streams=&#34;1.0:")[1:]

	video_id += [link[:11] for link in id_container]



video_link = ["http://youtube.com/watch?v="+ v_id for v_id in video_id]
#print video_link
### Downloading 

"""
c = 0
for v in video_link:
    c += 1
    os.system("youtube-dl -o "+str(c)+".mp4 -f 18 " + v)
"""    
