from bs4 import BeautifulSoup
import requests

url = 'https://www.google.com/search?q=bigchungus'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'lxml')

# Find by tag
title_tag = soup.find('title')

# Find by CSS class
divs = soup.find_all('div', class_='example')

# Find by id
specific_element = soup.find(id='unique-id')

# Using CSS selectors
elements = soup.select('div.example-class')
specific_element = soup.select_one('#unique-id')

text = title_tag.get_text()

link = soup.find('a')
href = link['href']

parent = link.parent
next_sibling = link.find_next_sibling('a')
