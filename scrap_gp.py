import requests
from bs4 import BeautifulSoup
import pandas as pd

# Fetch the webpage
page = requests.get("http://localhost:8000/products.html")
soup = BeautifulSoup(page.content, 'html.parser')

# Function to retrieve all products
def retrieve_all_products():
    return soup.find_all('li', class_='span4')

# Function to retrieve the first product price
def retrieve_first_product_price():
    all_products = retrieve_all_products()
    if all_products:
        product_one = all_products[0]
        product_one_price = product_one.find("strong")
        return product_one_price.get_text().strip().strip('$')
    return None

# Function to compare products
def lazy_comparator():
    all_products = retrieve_all_products()
    products = {}
    for product in all_products:
        product_name = product.find("p").get_text().strip()
        product_price = product.find("strong").get_text().strip().strip('$')
        products[product_name] = float(product_price)
    return sorted([(v, k) for k, v in products.items()])

# Extract product details and save to CSV
def extract_to_csv():
    all_products = retrieve_all_products()
    product_list = []

    for product in all_products:
        product_name = product.find("p").get_text().strip()
        product_price = product.find("strong").get_text().strip().strip('$')
        product_list.append({"Product Name": product_name, "Price": float(product_price)})

    # Convert to DataFrame
    df = pd.DataFrame(product_list)
    # Save to CSV
    df.to_csv('products.csv', index=False)

if __name__ == '__main__':
    print(soup.prettify())
    print(retrieve_first_product_price())
    print(lazy_comparator())
    extract_to_csv()
