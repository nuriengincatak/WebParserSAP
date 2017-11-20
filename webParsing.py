from bs4 import BeautifulSoup
import requests, time
import xlwt
import datetime
from dateutil import parser
from practice_python.german_pie import germanpie

wb = xlwt.Workbook()
sheet = wb.add_sheet("New Sheet", cell_overwrite_ok=True)

text = []
links = []
german = []
dates = []
jobID = []
print("          --SAP Job Lister--\nOne page takes around 30 seconds\nSAP.xls file will be created on the same folder")
print("Your sheet will have Name + date + Ad ID + link and german requirements" )
number = int(input("How many pages would you like to have? \n"))
keyword_main = "Working student"      #  str(input("What is the main keyword you would like to have? \n"))
keyword = str(input("What is the keyword you would like to have? (case-sensitive)\n"))
print("Please wait %d seconds" % (number*30))

rawurl= 'https://jobs.sap.com/search/?q=' + str(keyword_main) + '&locationsearch=walldorf&sortColumn=referencedate&sortDirection=desc&startrow='
for x in range(0, number):
    url = rawurl + str(x*25)
    r=requests.get(url)

    #r_html = r.text

    soup = BeautifulSoup(r.content, "lxml")

    #print(soup.find_all(name="span"))
    for link in soup.find_all(class_="jobTitle-link"):
        text.append(link.text) #name of the ad
        fullLinks = "https://jobs.sap.com" + link['href']
        links.append(fullLinks) # link of the ad
        lenLink = len(fullLinks)
        jobID.append(fullLinks[lenLink - 10:lenLink - 1])  # job Id is at the end of the link

    dateList = soup.find_all(class_="jobDate")[0::2]  # they are taking two times in a row, so we skip each one
    for j in range(1, len(dateList)):

        str1 = parser.parse(dateList[j].text).date()
        dates.append(str1)
        # print(dateList[j].text)

ger = germanpie
for y in range(0, len(links)):
    time.sleep(0.5)
    german.append(ger.german_checker(ger, links[y], keyword))  #searching for the keyword in each ad

 #to eliminate the first empty one


length = len(links)
"""
for i in range(0, length):
    print(text[i])
    print(links[i])
    time.sleep(1) #waits 2 secons to prevent the server from suspending
    print(german_checker(links[i]))
"""
print("total number of jobs that has been processed is: " + str(len(links)))



#todo add the job ads' ID number

for row_index in range(0, len(text)):
    sheet.write(row_index, 0, text[row_index])
    sheet.write(row_index, 1, dates[row_index])
    sheet.write(row_index, 3, jobID[row_index])
    sheet.write(row_index, 4, links[row_index])
    sheet.write(row_index, 2, german[row_index])

wb.save("SAP.xls")




