from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import pandas as pd
import urllib
from concurrent.futures import ThreadPoolExecutor

def select_driver():
    if os.environ.get('REMOTE_SERVER') == "1":
        print(f"REMOTE_SERVER: {os.environ.get('REMOTE_SERVER')}")
        hub_url = os.getenv("SELENIUM_HUB_URL", "http://my-selenium-grid-driver:4444/wd/hub")
        driver = webdriver.Remote(command_executor=hub_url, options=webdriver.ChromeOptions())
        print("ChromeDriver version:", driver.capabilities['chrome']['chromedriverVersion'])
        print("Driver ready!")
    else:
        print("REMOTE_SERVER: 0")
        print("installing ChromeDriverManager")
        service = Service(ChromeDriverManager().install())
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(service=service, options=chrome_options) 
        print("ChromeDriverManager installed!")
    return driver


def scrape_ingredient(ingredient):
    # options = Options()
    # options.headless = True
    # options.add_argument("--window-size=1920,1200")
    # options.add_argument('--disable-dev-shm-usage')
    print(f"Scraping {ingredient}")
    driver = select_driver()
    base_url = "https://groceries.asda.com/search/"

    full_url = base_url + urllib.parse.quote(ingredient)
    driver.get(full_url)

    time.sleep(10)  # Adjust the sleep duration based on your network speed and page load time

    product_elements = driver.find_elements(By.CLASS_NAME, "co-product")
    print("product element found")

    product_names = []
    product_links = []

    for product_element in product_elements:
        product_name_element = product_element.find_element(By.CLASS_NAME, "co-product__title").find_element(
            By.TAG_NAME, "a")
        product_name = product_name_element.text
        product_names.append(product_name)

        product_link = product_name_element.get_attribute("href")
        product_links.append(product_link)

    driver.quit()

    return {'ingredient_name': ingredient, 'products': [{'product_name': name, 'product_link': link} for name, link in
                                                        zip(product_names, product_links)]}


def scrape_asda(recipe_ingredients):
    with ThreadPoolExecutor() as executor:
        results = executor.map(scrape_ingredient, recipe_ingredients)

    all_data_df = pd.DataFrame()
    all_data_list = list(results)
    for data in all_data_list:
        ingredient_df = pd.DataFrame(data['products'])
        ingredient_df['ingredient_name'] = data['ingredient_name']
        all_data_df = pd.concat([all_data_df, ingredient_df], ignore_index=True)

    all_data_df.to_csv("asda_ingredients.csv")

    return all_data_list


def scrape_asda_first_product(ingredient):

    driver = select_driver()

    base_url = "https://groceries.asda.com/search/"

    full_url = base_url + urllib.parse.quote(ingredient)
    driver.get(full_url)

    time.sleep(10)  # Adjust the sleep duration based on your network speed and page load time
    
    product_element = driver.find_element(By.CLASS_NAME, "co-product")
    product_name_element = product_element.find_element(By.CLASS_NAME, "co-product__title").find_element(By.TAG_NAME, "a")
    product_name = product_name_element.text
    
    driver.quit()
    
    return {'ingredient_name': ingredient, 'first_product_name': product_name}

