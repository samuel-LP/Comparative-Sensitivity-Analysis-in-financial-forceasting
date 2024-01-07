from initialize_driver import make_driver
from open_NYT import login_to_nyt
from URLs import save_URLs

if __name__ == "__main__":

    driver = make_driver()
    URL = "https://www.nytimes.com/search?query=exxon+mobil"
    login_to_nyt(driver, URL)
    CSV_NAME = "URLs_exxon"
    CLICK_COUNT = 50
    save_URLs(driver, CSV_NAME, CLICK_COUNT)
