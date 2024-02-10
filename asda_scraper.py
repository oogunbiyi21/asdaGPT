from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import urllib


def scrape_asda(recipe_ingredients):
    options = Options()
    options.add_argument("--headless")
    options.headless = True
    options.add_argument("--window-size=1920,1200")

    print("installing ChromeDriverManager")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    print("ChromeDriverManager installed!")

    base_url = "https://groceries.asda.com/search/"

    all_data_df = pd.DataFrame()
    all_data_list = []

    for ingredient in recipe_ingredients:

        full_url = base_url + urllib.parse.quote(ingredient)
        driver.get(full_url)

        # Wait for the search results to load
        time.sleep(10)  # Adjust the sleep duration based on your network speed and page load time

        # Scrape the product information from the search results
        product_elements = driver.find_elements(By.CLASS_NAME, "co-product")
        print("product element found")

        # Create lists to store product names and links
        product_names = []
        product_links = []

        product_count = 0
        for product_element in product_elements:
            # Extract product name
            product_name_element = product_element.find_element(By.CLASS_NAME, "co-product__title").find_element(
                By.TAG_NAME, "a")
            product_name = product_name_element.text
            product_names.append(product_name)

            # Extract product link
            product_link = product_name_element.get_attribute("href")
            product_links.append(product_link)
            print(product_link)

            # Count product
            product_count += 1

        # add to dict
        ingredient_data = {
            'ingredient_name': ingredient,
            'products': [{'product_name': name, 'product_link': link} for name, link in
                         zip(product_names, product_links)]
        }

        # Create a DataFrame for the current page
        ingredient_name_for_df = [ingredient] * product_count
        ingredient_df = pd.DataFrame({'ingredient_name': ingredient_name_for_df,
                                      'product_name': product_names,
                                      'product_link': product_links})


        all_data_list.append(ingredient_data)
        all_data_df = all_data_df.append(ingredient_df, ignore_index=True)

    all_data_df.to_csv("asda_ingredients.csv")
    print(all_data_df)
    driver.quit()
    return all_data_list

