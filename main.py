from flask import Flask, render_template, request, send_from_directory
from asda_scraper_multithread import scrape_asda 
import socket
import os
from selenium import webdriver

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/scrape', methods=['GET', 'POST'])
def scrape():
    if request.method == 'GET':
        ingredients = request.args.get('ingredients')
        if ingredients:
            ingredients_list = [ingredient.strip() for ingredient in ingredients.split(',')]

            # Call scraper function
            scraped_data = scrape_asda(ingredients_list)

            return render_template('result.html', data=scraped_data)

    if request.method == 'POST':
        ingredients = request.form.get('ingredients')
        ingredients_list = [ingredient.strip() for ingredient in ingredients.split(',')]

        # Call scraper function
        scraped_data = scrape_asda(ingredients_list)

        return render_template('result.html', data=scraped_data)


@app.route('/.well-known/ai-plugin.json')
def serve_ai_plugin():
    return send_from_directory('.',
                               'ai-plugin.json',
                               mimetype='application/json',)


@app.route('/swagger.yaml')
def serve_openapi_yaml():
    return send_from_directory('.', 'swagger.yaml', mimetype='text/yaml')


# Health check endpoint
@app.route('/health')
def health_check():
    return '', 200


# selenium webservice check
@app.route('/selenium-check')
def selenium_check():
    hub_url = os.getenv("SELENIUM_HUB_URL", "http://my-selenium-grid-driver:4444/wd/hub")
    driver = webdriver.Remote(command_executor=hub_url, options=webdriver.ChromeOptions())
    print("ChromeDriver version:", driver.capabilities['chrome']['chromedriverVersion'])
    print("Driver ready!")

    return '', 200

if __name__ == "__main__":
    if os.environ.get('REMOTE_SERVER') == "1":
        print(f"REMOTE SERVER = {os.environ.get('REMOTE_SERVER')}")
        print("remote session")
    else:
        print("local session")
    app.run(host='0.0.0.0', port=81)
