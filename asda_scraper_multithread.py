from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import pandas as pd
import urllib
from concurrent.futures import ThreadPoolExecutor
import threading
import openai


# Thread-local storage for Chromedriver instances
thread_local = threading.local()

def select_driver():
    # Check if a Chromedriver instance is already assigned to the current thread
    if not hasattr(thread_local, "driver") or thread_local.driver is None:
        if os.environ.get('REMOTE_SERVER') == "1":
            print(f"REMOTE_SERVER: {os.environ.get('REMOTE_SERVER')}")
            hub_url = os.getenv("SELENIUM_HUB_URL", "http://my-selenium-grid-driver:4444/wd/hub")
            driver = webdriver.Remote(command_executor=hub_url, options=webdriver.ChromeOptions())
            thread_local.driver = driver
            print("ChromeDriver version:", driver.capabilities['chrome']['chromedriverVersion'])
            print("Driver ready!")
        else:
            print("REMOTE_SERVER: 0")
            print("installing ChromeDriverManager")
            try:
                service = Service(ChromeDriverManager().install())
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--disable-gpu')
                driver = webdriver.Chrome(service=service, options=chrome_options)
                thread_local.driver = driver
                print("ChromeDriverManager installed!")
            except Exception as e:
                print(f"Error installing ChromeDriverManager: {e}")
                print("ChromeDriverManager not installed!")
                raise e
    return thread_local.driver


def scrape_ingredient(ingredient):

    retries = 3
    for _ in range(retries):
        try:
            print(f"Scraping {ingredient}")
            driver = select_driver()
            base_url = "https://groceries.asda.com/search/"

            full_url = base_url + urllib.parse.quote(ingredient)
            driver.get(full_url)

            time.sleep(10)  # Adjust the sleep duration based on your network speed and page load time

            product_elements = driver.find_elements(By.CLASS_NAME, "co-product")
            print("product element found")

            products = []

            for product_element in product_elements:
                product_name_element = product_element.find_element(By.CLASS_NAME, "co-product__title").find_element(By.TAG_NAME, "a")
                product_name = product_name_element.text
                product_link = product_name_element.get_attribute("href")
                products.append({'product_name': product_name, 'product_link': product_link})

            driver.quit()
            return {'ingredient_name': ingredient, 'products': products}
            
        except WebDriverException as e:
            print(f"WebDriverException occurred: {e}")
            if _ < retries - 1:
                print(f"Retrying {ingredient}...")
                time.sleep(5)  # Wait before retrying
            else:
                print(f"Failed to scrape {ingredient} after {retries} retries.")
                return {'ingredient_name': ingredient, 'products': []}
        finally:
            if hasattr(thread_local, "driver") and thread_local.driver:
                thread_local.driver.quit()
                thread_local.driver = None
    
def choose_best_product(ingredient_data, recipe):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    ingredient_name = ingredient_data['ingredient_name']
    products = ingredient_data['products']
    
    example = """Based on the recipe, the best product for the ingredient 'Onion' would be: 
    <strong>Product Name:</strong> ASDA 3 Crunchy & Fragrant Brown Onions 
    <strong>Product Link:</strong> <a href="https://groceries.asda.com/product/onions-leeks/asda-3-crunchy-fragrant-brown-onions/910003012588">ASDA 3 Crunchy & Fragrant Brown Onions</a>. 
    Explanation: These brown onions are suitable for sautéing with other vegetables in the recipe. They provide a balanced flavor profile and are commonly used in cooking savory dishes like jollof rice. The pack size of 3 onions should provide an appropriate amount for the recipe, and their crunchy and fragrant nature will enhance the overall taste of the dish.
    """

    prompt = f"""Given the following recipe:\n\n{recipe}\n\nAnd the following products for the ingredient '{ingredient_name}', please choose the best one for the recipe. You must choose from the provided products and no other. Provide the product name and link in HTML format as follows: 

    Based on the recipe, the best product for the ingredient '{ingredient_name}' would be: 
    <strong>Product Name:</strong> [PRODUCT_NAME] 
    <strong>Product Link:</strong> <a href="[PRODUCT_LINK]">[PRODUCT_NAME]</a>. 
    Explanation: [EXPLANATION]

    Here is an example format for the ingredient 'Onion':

    {example}

    Ensure that only products from the product list are chosen. Now, please choose the best product from the list below and provide it in the format shown above with an explanation on why this product is suitable for the recipe:\n\n"""

    for product in products:
        prompt += f"Product Name: {product['product_name']}\nProduct Link: {product['product_link']}\n\n"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message['content'].strip()


def scrape_asda(recipe_ingredients, recipe):
    with ThreadPoolExecutor() as executor:
        results = executor.map(scrape_ingredient, recipe_ingredients)

    all_data_list = list(results)
    best_products = []

    for data in all_data_list:
        if data['products']:
            best_product = choose_best_product(data, recipe)
            best_products.append(best_product)

    return best_products


def scrape_asda_first_product(ingredient):

    driver = select_driver()

    base_url = "https://groceries.asda.com/search/"

    full_url = base_url + urllib.parse.quote(ingredient)
    driver.get(full_url)

    time.sleep(60)  # Adjust the sleep duration based on your network speed and page load time

    product_element = driver.find_element(By.CLASS_NAME, "co-product")
    product_name_element = product_element.find_element(By.CLASS_NAME, "co-product__title").find_element(By.TAG_NAME, "a")
    product_name = product_name_element.text
    
    driver.quit()
    
    return [{'ingredient_name': ingredient, 'first_product_name': product_name}]

