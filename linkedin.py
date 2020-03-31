import csv
from parsel import Selector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

USERNAME = input("Please enter your Linkedin email: ")
PASSWORD = input("Please enter your password: ")

writer = csv.writer(open('testing.csv', 'w')) # preparing csv file to store parsing result later
writer.writerow(['name', 'job_title', 'schools', 'location', 'ln_url'])

driver = webdriver.Firefox()

driver.get('https://www.linkedin.com/')

driver.find_element_by_xpath('//a[text()="Sign in"]').click()

username_input = driver.find_element_by_name('session_key')
username_input.send_keys(USERNAME)

password_input = driver.find_element_by_name('session_password')
password_input.send_keys(PASSWORD)

# click on the sign in button
# we're finding Sign in text button as it seems this element is seldom to be changed
driver.find_element_by_xpath('//button[text()="Sign in"]').click()

try:
  driver.find_element_by_xpath('//button[text()="Skip"]').click()
except:
  print("WARNING: No skip procedure") 

driver.get(input("Please enter a link of a Linkedin user to add to this file"))

try:
    sel = Selector(text=driver.page_source)
    name = sel.xpath('//title/text()').extract_first().split(')')[1].split('|')[0].strip().split(' ')
    first_name = name[0]
    last_name = name[1]
    job_title = sel.xpath('//div[1]/h2/text()').extract_first().strip()
    company = sel.xpath('//p[2]/text()').extract_first().strip()

    schools = ', '.join(sel.xpath('//*[contains(@class, "pv-entity__school-name")]/text()').extract())
    location = sel.xpath('//*[@class="t-16 t-black t-normal inline-block"]/text()').extract_first().strip()
    ln_url = driver.current_url
except:
    print('Failed to find user.')

print('\n')
print(first_name)
print(last_name)
print(company)
print(schools)
print(location)
print(ln_url)
print('\n')

writer.writerow([name, job_title, schools, location, ln_url])