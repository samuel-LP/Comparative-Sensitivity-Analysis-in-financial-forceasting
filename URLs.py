from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time
from numpy.random import normal
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


def save_URLs(driver: webdriver, output_file: str, click_count: int):
    try:

        df_existing = pd.read_csv(f"{output_file}.csv")
        existing_urls = set(df_existing['URL'])
    except FileNotFoundError:

        existing_urls = set()

    unique_urls = set(existing_urls)
    counter_click = 0

    time.sleep(abs(normal(1, 3)))

    while counter_click < click_count:
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, "html.parser")
        articles = soup.select("div.css-e1lvw9")

        for article in articles:
            link = article.find("a")
            if link:
                href = link.get("href")
                full_url = f'https://www.nytimes.com/{href}'  # Remplacez 'https://example.com' par la base de l'URL

                if full_url not in unique_urls:
                    unique_urls.add(full_url)

        df = pd.DataFrame({"URL": list(unique_urls)})
        df.to_csv(f"{output_file}.csv", index=False)

        print(f"Click {counter_click + 1}: {len(unique_urls)} liens ajoutés")

        try:
            show_more_button = driver.find_element(
                By.XPATH, '//*[@id="site-content"]/div/div[2]/div[3]/div/button'
            )
            show_more_button.click()
            time.sleep(abs(normal(0, 5)))
            counter_click += 1
        except NoSuchElementException:
            print("Fin")
            break

    print("Données récupérées")
    time.sleep(5)
    driver.quit()
