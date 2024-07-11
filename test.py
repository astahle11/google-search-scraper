from selenium import webdriver
from selenium.webdriver.common.by import By



url = "https://www.google.com/search?q=cats"


driver = webdriver.Chrome()

driver.get(url)
next = driver.find_element(By.ID, 'pnnext')
next.click()
next_page_url = driver.current_url

print(next_page_url)