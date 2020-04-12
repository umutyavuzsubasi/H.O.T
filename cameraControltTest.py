from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome(chrome_options=options)
driver.get("http://192.168.137.220:8080/settings_window.html")
button = driver.find_element_by_id('flashbtn')
button.click()
