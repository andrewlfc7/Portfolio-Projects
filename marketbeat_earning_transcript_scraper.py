
import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import sqlite3


driver = webdriver.Chrome()
driver.get("https://www.marketbeat.com/earnings/transcripts/")
search_box = driver.find_element(By.XPATH, '//*[@id="cphPrimaryContent_txtCompany"]')
# enter the search term
stock = input("Enter Symbol: ")


#search_term = ('GS')

search_box.send_keys(stock)

# submit the form
search_box.submit()

transcript = driver.find_element(By.XPATH,'//*[@id="cphPrimaryContent_pnlFilterTable"]/div[3]/div/table/tbody/tr[1]/td[3]')

transcript.click()


link = transcript.get_attribute("data-clean")


transcript_url = driver.current_url



data = requests.get(link)

data

soup = BeautifulSoup(data.text, 'html.parser')

executives_header = soup.find('h3', text='Corporate Executives')
executives = executives_header.find_next_sibling('ul', class_='pl-0')

presentation_header = soup.find('h2', text='Presentation')
presentation_discussion = presentation_header.find_next_sibling('div', class_='transcript-discussion')


Q_A_header= soup.find('h2', text='Questions and Answers')
Q_A_discussion = Q_A_header.find_next_sibling('div', class_='transcript-discussion')



# Close the browser
driver.quit()







link


presentation_discussion.text
Q_A_discussion.text
executives = executives.text


presentation = []
paragraphs = presentation_discussion.find_all('p')
for p in paragraphs:
    presentation.append(p.text)

q_a = []
paragraphs = Q_A_discussion.find_all('p')
for p in paragraphs:
    q_a.append(p.text)


presentation = " ".join(presentation)
q_a = " ".join(q_a)



# Connect to a database (create the database if it doesn't exist)
conn = sqlite3.connect("earning_transcript.db", timeout=10)

# Create a table for the transcripts
conn.execute('''CREATE TABLE IF NOT EXISTS transcript (presentation TEXT, executives TEXT, q_a TEXT, stock TEXT)''')


# Insert the data into the table
conn.execute("INSERT INTO transcript (presentation, executives, q_a,stock) VALUES (?, ?, ?,?)", (presentation, executives, q_a,stock))



# Commit the changes and close the connection
conn.commit()
