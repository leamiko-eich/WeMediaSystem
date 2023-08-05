from selenium import webdriver
from selenium.webdriver.common.by import By
driver = webdriver.Chrome()
driver.get("https://www.baidu.com/")
driver.find_element(By.ID, "kw").click()
driver.find_element(By.ID, "kw").send_keys("hello world")
driver.find_element(By.ID, "su").click()
driver.quit()