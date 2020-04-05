import csv
from dataclasses import dataclass
import requests, time, random
from bs4 import BeautifulSoup
from selenium import webdriver

@dataclass
class User:
  stage: str
  firstname: str
  lastname: str
  company: str
  position: str
  resume: str
  location: str
  status: str

d = webdriver.Firefox()
d.get('https://www.linkedin.com')
conf = open('config.txt')
l = conf.readlines()
USERNAME = l[0]
PASSWORD = l[1]
QUERY = l[2]

# writer = csv.writer(open('testing.csv', 'w')) # preparing csv file to store parsing result later
# writer.writerow(['name', 'job_title', 'schools', 'location', 'ln_url'])

d.find_element_by_xpath('//a[text()="Sign in"]').click()

username_input = d.find_element_by_name('session_key')
username_input.send_keys(USERNAME)

password_input = d.find_element_by_name('session_password')
password_input.send_keys(PASSWORD)

# click on the sign in button
# we're finding Sign in text button as it seems this element is seldom to be changed
d.find_element_by_xpath('//button[text()="Sign in"]').click()

try:
  d.find_element_by_xpath('//button[text()="Skip"]').click()
  print("Logged in")
except:
  print("Continuing with procedure, successfully logged in") 

d.get(QUERY)

SCROLL_PAUSE_TIME = 5

# Get scroll height
last_height = d.execute_script("return document.body.scrollHeight")

for i in range(3):
  # Scroll down to bottom
  d.execute_script("window.scrollTo(0, document.body.scrollHeight);")

  # Wait to load page
  time.sleep(SCROLL_PAUSE_TIME)

  # Calculate new scroll height and compare with last scroll height
  new_height = d.execute_script("return document.body.scrollHeight")
  if new_height == last_height:
      break
  last_height = new_height

src = d.page_source
soup = BeautifulSoup(src, 'lxml')

# for testing purposes
with open("out.html", "w") as file:
    file.write(soup.prettify())

name_div = soup.find('div', {'class': 'flex-1 mr5'})

name_loc = name_div.find_all('ul')
name = name_loc[0].find('li').get_text().strip().split(' ')
firstname = name[0]
lastname = name[1]

print("First name: " + firstname)
print("Last name: " + lastname)

# writer.writerow([name, job_title, schools, location, ln_url])