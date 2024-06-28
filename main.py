from flask import Flask, render_template, request, send_from_directory, jsonify, redirect
from asda_scraper_multithread import scrape_asda, scrape_asda_first_product
import socket
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import openai

app = Flask(__name__)

# Configure OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    query = request.form.get('query')
    
    # Step 1: Get recipe text from ChatGPT
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Provide a recipe for: {query}"}
        ]
    )
    recipe = response['choices'][0]['message']['content'].strip()
    
    # Step 2: Ask ChatGPT to list out food items
    food_items_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"List the food items in the recipe only, with no other text. And just the type of food, no measurements: {recipe}"}
        ]
    )
    ingredients = food_items_response['choices'][0]['message']['content'].strip()
    print(ingredients)
    food_items = [ingredient.strip().lstrip('- ') for ingredient in ingredients.split('\n') if ingredient.strip()]
    print(food_items)

    # Step 3: Scrape ASDA using food items
    # scraped_data = scrape_asda(food_items)

    if food_items:
        scraped_data = scrape_asda(food_items)
    else:
        scraped_data = []
    
    # Redirect to results page with recipe and scraped data
    return render_template('result.html', recipe=recipe, data=scraped_data)


def extract_food_items(text):
    # Tokenize the text into words
    words = word_tokenize(text)
    # Perform Part-of-Speech (POS) tagging
    tagged_words = pos_tag(words)
    # Extract nouns (NN) and proper nouns (NNP) as potential food items
    food_items = [word for word, tag in tagged_words if tag in ['NN', 'NNP']]
    return food_items

@app.route('/.well-known/ai-plugin.json')
def serve_ai_plugin():
    return send_from_directory('.', 'ai-plugin.json', mimetype='application/json')

@app.route('/swagger.yaml')
def serve_openapi_yaml():
    return send_from_directory('.', 'swagger.yaml', mimetype='text/yaml')

@app.route('/health')
def health_check():
    return '', 200

@app.route('/selenium-check')
def selenium_check():
    hub_url = os.getenv("SELENIUM_HUB_URL", "http://my-selenium-grid-driver:4444/wd/hub")
    driver = webdriver.Remote(command_executor=hub_url, options=webdriver.ChromeOptions())
    driver.get("http://quotes.toscrape.com/")
    first_quote_text = driver.find_element(By.CSS_SELECTOR, '.quote span.text').text
    driver.quit()
    return first_quote_text, 200

@app.route('/asda-check')
def asda_check():
    ingredient = "tomato"
    result = scrape_asda_first_product(ingredient)
    return jsonify(result)

@app.route('/envir-check')
def envir_check():
    return os.getenv("REMOTE_SERVER", "0")

if __name__ == "__main__":
    print("running asda scraper flask app")
    if os.environ.get('REMOTE_SERVER') == "1":
        print(f"REMOTE SERVER = {os.environ.get('REMOTE_SERVER')}")
        print("remote session")
    else:
        print("local session")
    app.run(host='0.0.0.0', port=80)
