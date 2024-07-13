from flask import Flask, render_template, request, send_from_directory, jsonify, redirect
from asda_scraper_multithread import scrape_asda, scrape_asda_first_product, choose_best_product
import socket
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import openai
from tenacity import retry, stop_after_attempt, wait_fixed

app = Flask(__name__)

# Configure OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test_html')
def test_html():
    # Sample instructions and products (normally this would be scraped data)
    instructions = """
        Here is a recipe for Jollof rice:

        Ingredients:
        - 2 cups of long-grain parboiled rice
        - 1 can of tomato paste (about 6 oz)
        - 1 cup of chopped onions
        - 1 cup of chopped bell peppers
        - 2 cloves of minced garlic
        - 1 teaspoon of thyme
        - 1 teaspoon of curry powder
        - 1 teaspoon of smoked paprika
        - 1 teaspoon of ground ginger
        - 1 teaspoon of salt
        - 1 teaspoon of black pepper
        - 3 cups of chicken or vegetable broth
        - 1/4 cup of vegetable oil

        Instructions:
        1. Rinse the rice in cold water until the water runs clear, then drain and set aside.
        2. Heat the vegetable oil in a large pot over medium heat. Add the chopped onions, bell peppers, and minced garlic. Sauté until the onions are soft and translucent.
        3. Add the tomato paste to the pot and cook, stirring frequently, for about 5 minutes until the tomato paste darkens in color.
        4. Add the thyme, curry powder, smoked paprika, ground ginger, salt, and black pepper to the pot. Stir well to combine with the tomato paste mixture.
        5. Pour in the chicken or vegetable broth and bring to a boil.
        6. Once the mixture is boiling, add the rinsed rice to the pot. Stir well to combine with the tomato mixture.
        7. Lower the heat to a simmer, cover the pot, and let it cook for about 25-30 minutes, or until the rice is cooked through and all the liquid has been absorbed.
        8. Once the rice is cooked, fluff it with a fork and serve hot.

        Enjoy your delicious Jollof rice!
    """

    best_products = [
        'The best product for the recipe of Jollof rice would be: <strong>Product Name:</strong> Veetee Long Grain <strong>Product Link:</strong> <a href="https://groceries.asda.com/product/long-grain-basmati-microwave-rice/veetee-long-grain/1000288568002">Veetee Long Grain at Asda</a> Veetee Long Grain rice is the most suitable option for making Jollof rice based on the provided recipe.',
        'Product Name: ASDA Crisp & Fragrant Sweet Peppers 3 Pack (Colour may vary) Product Link: <a href="https://groceries.asda.com/product/tomatoes-peppers/asda-crisp-fragrant-sweet-peppers-3-pack-colour-may-vary/910003188356">ASDA Crisp & Fragrant Sweet Peppers 3 Pack</a> These sweet peppers will be a great choice for the Jollof rice recipe!',
        'For the Jollof rice recipe, the best product for the ingredient \'garlic\' would be the <strong>ASDA Loose Garlic 60mm+</strong>. <strong>Product Name:</strong> ASDA Loose Garlic 60mm+ <strong>Product Link:</strong> <a href="https://groceries.asda.com/product/garlic-ginger/asda-loose-garlic-60-mm/910001811823">ASDA Loose Garlic 60mm+</a> This product provides fresh garlic cloves which you can mince for the recipe, ensuring the authentic flavor of the dish.',
        'For the recipe of Jollof rice, the best curry powder option would be: <strong>Product Name:</strong> COOK by ASDA Medium Curry Powder <strong>Product Link:</strong> <a href="https://groceries.asda.com/product/spices/cook-by-asda-medium-curry-powder/910000407852">COOK by ASDA Medium Curry Powder</a> This medium curry powder will provide a balanced flavor profile to complement the other ingredients in the dish. Enjoy making your delicious Jollof rice!',
        'For the recipe for Jollof rice, the best product for the ingredient \'ground ginger\' would be: <strong>Product Name:</strong> Schwartz Ginger Ground 26g <strong>Product Link:</strong> <a href="https://groceries.asda.com/product/spices/schwartz-ginger-ground-26-g/390001">Schwartz Ginger Ground 26g</a> This product will provide you with the high-quality ground ginger needed to enhance the flavor of your Jollof rice.',
        'The best product for the Jollof rice recipe is the "<strong>Baxters Favourites Chicken Broth</strong>." <strong>Product Name:</strong> Baxters Favourites Chicken Broth <strong>Product Link:</strong> <a href="https://groceries.asda.com/product/tinned-soup/baxters-favourites-chicken-broth/910000450864">Baxters Favourites Chicken Broth</a> This chicken broth will provide a flavorful base for your Jollof rice recipe. Enjoy cooking!'
    ]

    return render_template('result.html', instructions=instructions, best_products=best_products)


@app.route('/test_gpt_response')
def test_gpt_response():

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def get_best_product(data, recipe):
        return choose_best_product(data, recipe)

    # Sample instructions and products (normally this would be scraped data)
    instructions = """
        Sure! Here is a recipe for Jollof Rice, a popular West African dish:
        Ingredients:
        - 2 cups long-grain parboiled rice
        - 1 can (400g) of diced tomatoes
        - 1 medium-sized onion, chopped
        - 1 red bell pepper, chopped
        - 1 scotch bonnet pepper, chopped (adjust for spiciness)
        - 3 cloves of garlic, minced
        - 1 teaspoon ground ginger
        - 1 teaspoon curry powder
        - 1 teaspoon thyme
        - 1 teaspoon paprika
        - 1 teaspoon dried parsley
        - 1 teaspoon salt (adjust to taste)
        - 2 cups chicken or vegetable broth
        - 1/4 cup vegetable oil

        Instructions:
        1. Rinse the rice in cold water until the water runs clear, then set aside.
        2. In a blender, blend the diced tomatoes, onion, bell pepper, scotch bonnet pepper, and garlic until smooth.
        3. Heat the vegetable oil in a large pot over medium heat. Add the blended tomato mixture and cook for about 10-15 minutes, stirring occasionally until the mixture thickens.
        4. Add the ground ginger, curry powder, thyme, paprika, dried parsley, and salt to the tomato mixture. Stir well to combine.
        5. Add the chicken or vegetable broth to the pot and bring to a simmer.
        6. Add the rinsed rice to the pot and stir to combine with the tomato mixture.
        7. Cover the pot with a tight-fitting lid and reduce the heat to low. Let the rice cook undisturbed for about 25-30 minutes, or until the rice is cooked through and the liquid is absorbed.
        8. Once the rice is cooked, fluff it with a fork and adjust seasoning if necessary.
        9. Serve the Jollof Rice hot with your choice of protein like grilled chicken, fish, or tofu.

        Enjoy your homemade Jollof Rice!
    """

    ingredient_data_list = [
        {
            'ingredient_name': 'Long-grain parboiled rice',
            'products': [
                {'product_name': 'Tilda Everyday Long Grain Rice', 'product_link': 'https://groceries.asda.com/product/long-grain-basmati-rice/tilda-everyday-long-grain-rice/1000383170477'},
            ]
        },
        {
            'ingredient_name': 'Onion',
            'products': [
                {'product_name': 'ASDA 3 Crunchy & Fragrant Brown Onions', 'product_link': 'https://groceries.asda.com/product/onions-leeks/asda-3-crunchy-fragrant-brown-onions/910003012588'},
            ]
        },
    ]

    best_products = []
    for ingredient_data in ingredient_data_list:
        best_product_html = get_best_product(ingredient_data, instructions)
        best_products.append(best_product_html)

    return render_template('result.html', instructions=instructions, best_products=best_products)

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
    ingredient_example = """
    Eggs
    Cheese
    Ham
    """

    food_items_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"List the food items in the recipe only, with no other text, in a list. And just the type of food, no measurements. \nAn example: {ingredient_example}. \nThis the recipe: {recipe} \n Please provide the list of ingredients."}
        ]
    )
    ingredients = food_items_response['choices'][0]['message']['content'].strip()
    print(ingredients)
    food_items = [ingredient.strip().lstrip('- ') for ingredient in ingredients.split('\n') if ingredient.strip()]
    print(food_items)

    # Step 3: Scrape ASDA using food items
    # scraped_data = scrape_asda(food_items)

    if food_items:
        scraped_data = scrape_asda(food_items, recipe)
    else:
        scraped_data = []
    
    # Redirect to results page with recipe and scraped data
    print(recipe)
    print(scraped_data)
    return render_template('result.html', instructions=recipe, best_products=scraped_data)

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
