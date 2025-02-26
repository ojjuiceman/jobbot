import argparse, os, time
import urlparse, random
from selenium import webdriver
driver = webdriver.Chrome()

from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


def getPeopleLinks(page):
        links = []
        for link in page.find_all('a'):
            url = link.get('href')
            if url:
                    if 'profile/view?id=' in url:
                         links.append(url)
        return links

def getJobLinks(page):
        links = []
        for link in page.find_all('a'):
                url = link.get('href')
                if url:
                        if '/jobs' in url:
                                links.append(url)
                return links

def getID(url):
        pUrl = urlparse.urlparse(url)
        return urlparse.parse_qs(pUrl.query)['id'][0]

def ViewBot(browser):
        visited = {}
        pList = []
        count = 0
        while True:
                #sleep to make sure everything loads
                #add random to make us look human.
                time.sleep(random.uniform(3.5, 6.9))
                page = BeautifulSoup(browser.page_source)
                people = getPeopleLinks(page)
                if people:
                            for person in people:
                                ID = getID(person)
                                if ID not in visited:
                                        pList.append(person)
                                        visited[ID] = 1
        if pList:
                         person = pList.pop()
                         browser.get(person)
                         count += 1
        else: #otherwise find people via the job pages
                         jobs = getJobLinks(page)
                         if jobs:
                                 job = random.choice(jobs)
                                 root = 'http://www.linkedin.com'
                                 roots = 'http://www.linkedin.com'
                                 if root not in job or roots not in job:
                                    job = 'https://www.linkedin.com' + job
                                 browser.get(job)
                         else:
                                 print "Im lost exiting"
                                 sys.exit()

                          #output make otpion for this
                         print "[+] "+browser.title+" Visited! /n("\
                                  +str(count)+"/"+str(len(pList))+") Visited/Queue"
def Main():
        parser = argparse.ArgumentParser()
        parser.add_argument("email", help="linkedin email")
        parser.add_argument("password", help="linkedin password")
        args = parser.parse_args()

        browser = webdriver.Chrome()
        browser.get("https://linkedin.com/uas/login")

        emailElement = browser.find_element_by_id("session_key-login")
        emailElement.send_keys(args.email)
        passElement = browser.find_element_by_id("session_password-login")
        passElement.send_keys(args.password)
        passElement.submit()

        os.system('cls')
        print "[+] Success Logged in"
        ViewBot(browser)
        browser.close()

if __name__ == "__main__":
        Main()

