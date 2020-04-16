import csv
from dataclasses import dataclass
import time
from bs4 import BeautifulSoup
from selenium import webdriver

d = webdriver.Firefox()

conf = open('config.txt')
lines = conf.readlines()
# USERNAME = lines[0]
# PASSWORD = lines[1]
# QUERY = lines[2]
# FILENAME = lines[3]

def get_page_data(USERNAME, PASSWORD, QUERY, FILENAME):
    d.get('https://www.linkedin.com')
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
    with open("out.html", "w", encoding="utf-8") as file:
        file.write(soup.prettify())

    name_div = soup.find('div', {'class': 'flex-1 mr5'})

    name_loc = name_div.find_all('ul')
    name = name_loc[0].find('li').get_text().strip().split(' ')
    first_name = name[0]
    last_name = name[1]
    loc = name_loc[1].find('li').get_text().strip()
    profile_title = name_div.find('h2').get_text().strip()


    exp_section = soup.find('section', {'id': 'experience-section'})
    exp_section = exp_section.find('ul')
    li_tags = exp_section.find('div')
    a_tags = li_tags.find('a')

    # handling of alternate version of experience display
    if len(a_tags.find_all('p')) < 2:
        # special case
        company_name = exp_section.find_all('h3')[0].find_all('span')[1].get_text().strip()
        job_title = exp_section.find_all('h3')[1].find_all('span')[1].get_text().strip()
    else:
        job_title = a_tags.find('h3').get_text().strip()
        company_name = a_tags.find_all('p')[1].get_text().strip()

    print("First name: " + first_name)
    print("Last name: " + last_name)
    print("Location: " + loc)
    print("Position: " + job_title)
    print("Company Name: " + company_name)

    path = FILENAME + ".csv"

    row = ['primary', first_name, last_name, company_name, job_title, 'resume', loc, 'status']

    fields = ['stage', 'first_name', 'last_name', 'company', 'position', 'resume', 'location', 'status']

    with open(path, 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(fields)
        csv_writer.writerow(row)


d.close()
