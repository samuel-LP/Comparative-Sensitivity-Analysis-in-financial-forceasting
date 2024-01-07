from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from numpy.random import normal
import time


def login_to_nyt(driver: webdriver, url: str) -> webdriver:
    # url = "https://www.nytimes.com/search?query=General+Motors"
    driver.get(url)
    time.sleep(abs(normal(1, 3)))
    driver.implicitly_wait(4)
    # accept cookies

    cookies_button = driver.find_element(by="xpath",
                                         value='//*[@id="dock-container"]/div[2]/div/div/div[2]/button[1]'
    )
    cookies_button.click()
    time.sleep(abs(normal(1, 3)))
    # username = driver.find_element(
    #    by="xpath", value='//*[@id="email"]'
    # )
    # username.send_keys('samuelparientelaunay@gmail.com')

    # ime.sleep(abs(normal(1, 3)))

    # continue_button = driver.find_element(by="xpath",
    #                                       value='//*[@id="myAccountAuth"]/div/div/div/form/div/div[4]/button')

    # continue_button.click()

    # time.sleep(abs(normal(1, 3)))

    # password = driver.find_element(by="xpath",
    #                                value='//*[@id="password"]')

    # password.send_keys('SamuelBSamuelLAxel')

    # time.sleep(abs(normal(1, 3)))

    # loging_button = driver.find_element(by="xpath",
    #                                     value='//*[@id="myAccountAuth"]/div/div/form/div/div[2]/button')

    # loging_button.click()

    return driver
