recipe = "Your Jollof Rice recipe here"
ingredient_name = "Onion"
products = [
    {
        "product_name": "ASDA 3 Crunchy & Fragrant Brown Onions",
        "product_link": "https://groceries.asda.com/product/onions-leeks/asda-3-crunchy-fragrant-brown-onions/910003012588"
    },
    {
        "product_name": "Another Onion Product",
        "product_link": "https://groceries.asda.com/product/onions-leeks/another-onion-product/123456789"
    }
]

example = """Based on the recipe, the best product for the ingredient 'Onion' would be: 
<strong>Product Name:</strong> ASDA 3 Crunchy & Fragrant Brown Onions 
<strong>Product Link:</strong> <a href="https://groceries.asda.com/product/onions-leeks/asda-3-crunchy-fragrant-brown-onions/910003012588">ASDA 3 Crunchy & Fragrant Brown Onions</a>. 
Explanation: These brown onions are suitable for sautéing with other vegetables in the recipe. They provide a balanced flavor profile and are commonly used in cooking savory dishes like jollof rice. The pack size of 3 onions should provide an appropriate amount for the recipe, and their crunchy and fragrant nature will enhance the overall taste of the dish.
"""

prompt = f"""Given the following recipe:\n\n{recipe}\n\nAnd the following products for the ingredient '{ingredient_name}', please choose the best one for the recipe. Provide the product name and link in HTML format as follows: 

Based on the recipe, the best product for the ingredient '{ingredient_name}' would be: 
<strong>Product Name:</strong> [PRODUCT_NAME] 
<strong>Product Link:</strong> <a href="[PRODUCT_LINK]">[PRODUCT_NAME]</a>. 
Explanation: [EXPLANATION]

Here is an example format for the ingredient 'Onion':

{example}

Now, please choose the best product from the list below and provide it in the format shown above with an explanation on why this product is suitable for the recipe:\n\n"""

for product in products:
    prompt += f"Product Name: {product['product_name']}\nProduct Link: {product['product_link']}\n\n"

print(prompt)
